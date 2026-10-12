"""Rebuild the local review artifact without making API calls."""
import argparse
import html
import itertools
import json
import math
import random
import textwrap
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

import run_pilot as pilot

NAMES={"openai/gpt-4o-mini":"GPT-4o mini","openai/gpt-4.1-mini":"GPT-4.1 mini",
       "google/gemini-2.5-flash-lite":"Gemini Flash-Lite","anthropic/claude-haiku-4.5":"Claude Haiku 4.5"}
COLORS=["#376b68","#668142","#b56944","#736692"]

def agreement(values):
    n=len(values)
    return sum(k*(k-1) for k in Counter(values).values())/(n*(n-1)) if n>1 else None

def tv(left,right):
    a,b=Counter(left),Counter(right)
    return sum(abs(a[k]/len(left)-b[k]/len(right)) for k in a.keys()|b.keys())/2

def bootstrap(values):
    rng=random.Random(6700417)
    res=sorted(mean(rng.choices(values,k=len(values))) for _ in range(10000))
    return [res[249],res[9749]]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("run",type=Path)
    args=parser.parse_args();run=args.run
    manifest=json.loads((run/"manifest.json").read_text())
    status=json.loads((run/"run_status.json").read_text())
    recall_coding=json.loads((run/"recall_coding.json").read_text()) if (run/"recall_coding.json").exists() else None
    pilot.summarize(run,manifest,status)
    strict_results=json.loads((run/"results.json").read_text())
    strict_samples=pilot.load_lines(run/"samples.jsonl")
    raw=pilot.load_lines(run/"raw.jsonl")
    requests={e["id"]:e for e in raw if e["event"]=="request"}
    final_byjob={s["id"]:s for s in strict_samples}
    # Pre-decision quality check motivated this sensitivity analysis: a correct
    # label with a >60-word explanation must not silently become a different
    # sampled choice just because a retry was shorter. Preserve every raw output.
    samples=[]
    for event in raw:
        if event["event"]!="response" or event["attempt"]!=0:continue
        final=final_byjob.get(event["job"])
        if not final:continue
        try:
            parsed=json.loads(event["response"]["choices"][0]["message"]["content"])
            if final["kind"]=="decision":
                assert set(parsed)=={"choice","confidence","reason"}
                assert parsed["choice"] in final["mapping"]
                assert isinstance(parsed["reason"],str)
                assert isinstance(parsed["confidence"],(int,float)) and not isinstance(parsed["confidence"],bool)
                assert math.isfinite(parsed["confidence"]) and 0<=parsed["confidence"]<=1
                compliant=len(parsed["reason"].split())<=60
            else:
                assert set(parsed)=={"knows","description"} and isinstance(parsed["knows"],bool)
                assert isinstance(parsed["description"],str)
                compliant=len(parsed["description"].split())<=60
            record=dict(final,valid=True,parsed=parsed,attempt=0,source_request_id=event["id"],
                        format_compliant_first_attempt=compliant,analysis_policy="first_attempt_choice_valid",
                        usage=event["response"]["usage"],response_id=event["response"]["id"])
            if final["kind"]=="decision":record["canonical_choice"]=final["mapping"][parsed["choice"]]
            record.pop("error",None)
            samples.append(record)
        except (AssertionError,ValueError,KeyError,TypeError):
            continue
    sensitivity_dir=run/"first_attempt_choice_valid"
    sensitivity_dir.mkdir(exist_ok=True)
    (sensitivity_dir/"samples.jsonl").write_text("".join(json.dumps(s,ensure_ascii=False)+"\n" for s in samples))
    pilot.save(sensitivity_dir/"analysis_policy.json",dict(policy="first attempt only, retain schema-valid choices even when justification exceeds 60 words",
        rationale="Sensitivity analysis added after observing format noncompliance, before inspecting outcome aggregates. Not an original preregistered primary.",
        source="../raw.jsonl",warning="Original strict-format results remain in parent results.csv and summary.md. No new API calls."))
    pilot.summarize(sensitivity_dir,manifest,status)
    results=json.loads((sensitivity_dir/"results.json").read_text())
    decisions=[s for s in samples if s["kind"]=="decision" and s.get("valid")]
    models=manifest["models"];items=manifest["items"]
    matched={i["id"] for i in items if "R2" in manifest["conditions"][i["id"]]}
    n=manifest["n"]
    bycell=defaultdict(list)
    for s in decisions:bycell[(s["item"],s["model"],s["condition"],s["perturbation"])].append(s)
    indexed={(r["item"],r["model"],r["condition"]):r for r in results}
    def records(m,c,ids):
        return [r for r in results if r["model"]==m and r["condition"]==c and r["item"] in ids and r["complete"]]
    def stats(rr):
        numerator=sum(r["flip_numerator"] for r in rr);denominator=sum(r["flip_denominator"] for r in rr)
        return dict(repeat_agreement=mean(r["within_cell_pair_agreement"] for r in rr) if rr else None,
                    flip=numerator/denominator if denominator else None,flip_count=numerator,flip_denominator=denominator,
                    entropy=mean(r["mean_within_cell_entropy"] for r in rr) if rr else None,
                    ties=sum(r["tied_cells"] for r in rr),item_count=len(rr))
    matched_stats={m:{c:stats(records(m,c,matched)) for c in ("R0","R1","R2")} for m in models}
    all_stats={m:{c:stats(records(m,c,{i['id'] for i in items})) for c in ("R0","R1")} for m in models}
    blocks=[]
    for m in models:
        for c in ("R0","R1","R2"):
            for block in (0,1):
                aa=[]
                for id_ in sorted(matched):
                    for p in ("p0","p1","p2","p3"):
                        vv=[s["canonical_choice"] for s in bycell[(id_,m,c,p)] if s["sample"]//3==block]
                        if len(vv)==3:aa.append(agreement(vv))
                blocks.append(dict(model=m,condition=c,block=block+1,agreement=mean(aa) if aa else None,complete_cells=len(aa)))
    pair_deltas=[]
    for id_ in sorted(matched):
        vv=[]
        for m in models:
            a=indexed.get((id_,m,"R0"));b=indexed.get((id_,m,"R2"))
            if a and b and a["complete"] and b["complete"]:
                delta=b["within_cell_pair_agreement"]-a["within_cell_pair_agreement"]
                vv.append(delta)
                pair_deltas.append(dict(item=id_,model=m,delta=delta))
    story_deltas=[mean(r["delta"] for r in pair_deltas if r["item"]==id_) for id_ in sorted(matched)
                  if any(r["item"]==id_ for r in pair_deltas)]
    sensitivity=[]
    for m in models:
        for c in ("R0","R1","R2"):
            aa=[];within=[];tvv=[];tie_lower=[];tie_upper=[]
            for id_ in sorted(matched):
                base=[s["canonical_choice"] for s in bycell[(id_,m,c,"p0")]]
                if len(base)!=n:continue
                for p in ("p1","p2","p3"):
                    other=[s["canonical_choice"] for s in bycell[(id_,m,c,p)]]
                    if len(other)!=n:continue
                    a,b=Counter(base),Counter(other)
                    aa.append(sum(a[k]*b[k] for k in a.keys()|b.keys())/(n*n))
                    within.append((agreement(base)+agreement(other))/2)
                    tvv.append(tv(base,other))
                    bm,om=set(pilot.modal(base)[0]),set(pilot.modal(other)[0])
                    tie_lower.append(int(not bm.intersection(om)))
                    tie_upper.append(int(not (len(bm)==len(om)==1 and bm==om)))
            sensitivity.append(dict(model=m,condition=c,cross_prompt_agreement=mean(aa) if aa else None,
                excess_perturbation_disagreement=mean(w-a for w,a in zip(within,aa)) if aa else None,
                total_variation=mean(tvv) if tvv else None,flip_lower=mean(tie_lower) if aa else None,
                flip_upper=mean(tie_upper) if aa else None,pairs=len(aa)))
    between=[]
    for m1,m2 in itertools.combinations(models,2):
        for c in ("R0","R1","R2"):
            vv=[]
            for id_ in sorted(matched):
                for p in ("p0","p1","p2","p3"):
                    a=[s["canonical_choice"] for s in bycell[(id_,m1,c,p)]]
                    b=[s["canonical_choice"] for s in bycell[(id_,m2,c,p)]]
                    if len(a)==len(b)==n:
                        ca,cb=Counter(a),Counter(b)
                        vv.append(sum(ca[k]*cb[k] for k in ca.keys()|cb.keys())/(n*n))
            between.append(dict(first=m1,second=m2,condition=c,agreement=mean(vv) if vv else None,cells=len(vv)))
    shifts=[]
    for i in items:
        for m in models:
            a=indexed.get((i["id"],m,"R0"));b=indexed.get((i["id"],m,"R1"));c=indexed.get((i["id"],m,"R2"))
            shifts.append(dict(item=i["id"],model=m,R0=a["modal_choice"] if a else None,R1=b["modal_choice"] if b else None,R2=c["modal_choice"] if c else None))
    responses=[e for e in raw if e["event"]=="response"]
    audit=dict(valid_decisions=len(decisions),valid_recalls=sum(s["kind"]=="recall" and s.get("valid",False) for s in samples),
               strict_valid_decisions=sum(s["kind"]=="decision" and s.get("valid",False) for s in strict_samples),
               strict_valid_recalls=sum(s["kind"]=="recall" and s.get("valid",False) for s in strict_samples),
               first_attempt_word_limit_failures=sum(not s["format_compliant_first_attempt"] for s in samples),
               invalid_final=sum(not s.get("valid",False) for s in strict_samples),api_responses=len(responses),
               validation_failures=len(pilot.load_lines(run/"validation_errors.jsonl")),
               prompt_tokens=sum(e["response"].get("usage",{}).get("prompt_tokens",0) for e in responses),
               completion_tokens=sum(e["response"].get("usage",{}).get("completion_tokens",0) for e in responses),
               reasoning_tokens=sum(e["response"].get("usage",{}).get("completion_tokens_details",{}).get("reasoning_tokens",0) for e in responses),
               nonzero_reasoning_responses=sum(e["response"].get("usage",{}).get("completion_tokens_details",{}).get("reasoning_tokens",0)>0 for e in responses),
               unique_response_ids=len({e["response"].get("id") for e in responses}),
               providers=dict(Counter(e["response"].get("provider") for e in responses)))
    strict_comparison={}
    for m in models:
        common={id_ for id_ in matched if all(any(r["item"]==id_ and r["model"]==m and r["condition"]==c and r["complete"] for r in strict_results) for c in ("R0","R1","R2"))}
        strict_comparison[m]=dict(common_items=sorted(common),conditions={c:stats([r for r in strict_results if r["model"]==m and r["condition"]==c and r["item"] in common]) for c in ("R0","R1","R2")})
    analysis=dict(audit=audit,recall_manual_review=recall_coding,analysis_policy="first_attempt_choice_valid; word-limit deviations retained, not hidden",strict_complete_matched_sensitivity=strict_comparison,
                  matched_five_story=matched_stats,all_eight_story=all_stats,split_blocks=blocks,
                  item_model_R2_minus_R0=pair_deltas,story_clustered_mean_delta=mean(story_deltas) if story_deltas else None,
                  story_cluster_bootstrap_95=bootstrap(story_deltas) if story_deltas else None,
                  perturbation_sensitivity=sensitivity,between_model_agreement=between,modal_shifts=shifts,
                  note="Bootstrap is descriptive sensitivity with only five selected story clusters, not confirmatory population inference.")
    pilot.save(run/"analysis.json",analysis)

    plt.rcParams.update({"figure.facecolor":"#f7f5ee","axes.facecolor":"#f7f5ee","axes.spines.top":False,
                         "axes.spines.right":False,"font.size":10,"text.color":"#292d28","axes.labelcolor":"#292d28","svg.fonttype":"none"})
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout="constrained")
    for m,color in zip(models,COLORS):
        aa=[matched_stats[m][c]["repeat_agreement"] for c in ("R0","R1","R2")]
        ff=[matched_stats[m][c]["flip"] for c in ("R0","R1","R2")]
        axes[0].plot(range(3),[100*x if x is not None else math.nan for x in aa],marker="o",lw=2,color=color,label=NAMES[m])
        axes[1].plot(range(3),[100*x if x is not None else math.nan for x in ff],marker="o",lw=2,color=color,label=NAMES[m])
    for ax in axes:
        ax.set_xticks(range(3),["Short\n80–120 words","Synopsis\n600–800 words","Full pre-decision\ntext"])
        ax.set_ylim(-2,102);ax.grid(axis="y",alpha=.2);ax.set_ylabel("Percent")
    axes[0].set_title("Repeatability: higher means more stable",loc="left",pad=14)
    axes[1].set_title("Perturbation flips: lower means more stable",loc="left",pad=14)
    axes[0].legend(loc="lower left",frameon=False,fontsize=9)
    fig.suptitle("Same five stories, four models — not a moral-quality score\nFirst-attempt choices, including length-only format failures",fontsize=12)
    fig.savefig(run/"stability.svg");fig.savefig(run/"stability.png",dpi=180);plt.close(fig)

    data=[[100*next((r["delta"] for r in pair_deltas if r["item"]==id_ and r["model"]==m),math.nan) for m in models] for id_ in sorted(matched)]
    fig,ax=plt.subplots(figsize=(9,4.8),layout="constrained")
    im=ax.imshow(data,cmap="BrBG",norm=TwoSlopeNorm(vmin=-50,vcenter=0,vmax=50),aspect="auto")
    ax.set_xticks(range(len(models)),[textwrap.fill(NAMES[m],width=13) for m in models],fontsize=9)
    ax.set_yticks(range(len(matched)),[textwrap.fill(next(i["title"] for i in items if i["id"]==id_),width=28) for id_ in sorted(matched)],fontsize=9)
    for y,row in enumerate(data):
        for x,value in enumerate(row):
            ax.text(x,y,f"{value:+.1f}" if math.isfinite(value) else "—",ha="center",va="center",color="white" if abs(value)>30 else "#242924",fontsize=11)
    ax.set_title("Full text minus short vignette: repeat-agreement change",loc="left",pad=14)
    fig.colorbar(im,ax=ax,label="Percentage points · positive = more repeatable",shrink=.8)
    fig.savefig(run/"item_changes.svg");fig.savefig(run/"item_changes.png",dpi=180);plt.close(fig)

    def pct(x):return "—" if x is None else f"{x:.1%}"
    lines=["# Initial assessment: context richness and decision stability","",f"**{status['state']}** — {audit['valid_decisions']:,} first-attempt schema-valid choices, {audit['valid_recalls']} readable recall checks. Run spend **${status['run_cost']:.4f}**; cumulative including preflights **${status['budget']['actual']:.4f} / $5**.","","See [the plain-language interpretation](interpretation.md) for the bottom line and concrete examples.",
           "",f"**Important analysis distinction:** {audit['strict_valid_decisions']} decision jobs passed the full strict rule after at most one retry. The charts below instead use every schema-valid **first choice**, retaining {audit['first_attempt_word_limit_failures']} first-attempt explanations that exceeded 60 words. This format-robust sensitivity analysis was added after observing length failures, before viewing aggregate choice outcomes. It avoids outcome-dependent resampling through format retries; it is not the originally specified strict analysis. Original strict metrics remain in `summary.md` / `results.csv`, with a matched-complete strict comparison in `analysis.json`.",
           "","## What was tested","","Eight public-domain stories; four smaller models; six responses to each identical prompt at temperature 0.7. Four prompt versions test canonical wording, option order, question paraphrase, and numeric labels. Five short stories receive R0/R1/R2; the other three receive only R0/R1. These are hypothetical decisions, not real agent trajectories.",
           "","## Matched five-story panel","","Pairwise repeat agreement asks: if we draw two responses to exactly the same prompt, how often do they choose the same action? It is not a judgment of whether that action is good.","","| Model | Short | Synopsis | Full text | Full − short |","|---|---:|---:|---:|---:|"]
    for m in models:
        a=[matched_stats[m][c]["repeat_agreement"] for c in ("R0","R1","R2")]
        lines.append(f"| {NAMES[m]} | {pct(a[0])} | {pct(a[1])} | {pct(a[2])} | {(a[2]-a[0])*100:+.1f} pp |")
    if story_deltas:
        ci=analysis["story_cluster_bootstrap_95"]
        lines += ["",f"Equal-weighted model/story mean full-minus-short change: **{mean(story_deltas)*100:+.1f} percentage points**. Descriptive five-story cluster-bootstrap range: **{ci[0]*100:+.1f} to {ci[1]*100:+.1f} pp**. This range is unstable with five selected stories and is not a general population claim."]
    lines += ["","![Stability](stability.png)","","![Item-level changes](item_changes.png)","","## Perturbation flips and ties","","| Model | Short | Synopsis | Full text |","|---|---|---|---|"]
    for m in models:
        cc=[matched_stats[m][c] for c in ("R0","R1","R2")]
        lines.append("| "+" | ".join([NAMES[m]]+[f"{r['flip_count']}/{r['flip_denominator']} ({pct(r['flip'])})" for r in cc])+" |")
    lines += ["","A flip compares a perturbed prompt's modal choice with the canonical prompt's modal choice. Tied modes are excluded rather than arbitrarily resolved. With six samples, ties can be common: see `analysis.json` for tie-inclusive lower/upper flip bounds and distribution-level sensitivity. The primary flip metric is noisy at this sample size.",
              "","## Split-half check","","The two blocks of three were fixed before the run and interleaved in time. A matching direction in both is more reassuring than a pooled effect alone; neither block is an independent set of stories.","","| Model | Block 1 short → full | Block 2 short → full |","|---|---|---|"]
    for m in models:
        vals=[]
        for b in (1,2):
            vv=[next(r["agreement"] for r in blocks if r["model"]==m and r["block"]==b and r["condition"]==c) for c in ("R0","R2")]
            vals.append(f"{pct(vv[0])} → {pct(vv[1])}")
        lines.append("| "+" | ".join([NAMES[m]]+vals)+" |")
    lines += ["","## Author recall and interpretation","","Read the 32 recall descriptions in `summary.md` and the browser report. Self-reported familiarity is not verified memory and does not establish that it caused a decision. Jekyll has no exact author-choice mapping; Postmaster has overlapping B/C canon actions. The full texts also expose characters' prior commitments, so apparent stability can mean role imitation, stronger constraints, or better information—not a steadier moral compass.",
              "","## Strict-format sensitivity","","| Model | Common complete stories | Short agreement | Synopsis | Full |","|---|---:|---:|---:|---:|"]
    for m in models:
        sc=strict_comparison[m]
        lines.append("| "+" | ".join([NAMES[m],str(len(sc["common_items"]))]+[pct(sc["conditions"][c]["repeat_agreement"]) for c in ("R0","R1","R2")])+" |")
    if recall_coding:
        rc=recall_coding["summary"]
        lines += ["","## Source-checked recall review","",f"The coding assistant compared first attempts with source continuations: {rc['claimed_knows']}/{rc['probes']} claimed familiarity; {rc['named_broad_core_action']}/{rc['probes']} named the broad author action; {rc['claimed_knows_but_wrong_core']} affirmative claims were wrong about the core action; {rc['honest_unknown']} admitted not knowing. Correct broad actions sometimes came with invented details. This is not independent human adjudication: see `recall_coding.json` for the criteria and specific errors.",
                  "","A validator bug unnecessarily rejected an empty description accompanying `knows=false`, causing needless retries. The original responses and charges are retained, the validator is fixed and regression-tested, and this review uses first attempts. See `interpretation.md` for the consequences in this run."]
    lines += ["","This strict-format table uses only stories complete in all three arms for that model. It can be a much smaller, selectively retained panel; do not compare it as if every model still had all five stories.",
              "","## Quality audit","",f"{audit['api_responses']} billed response attempts; {audit['validation_failures']} validation failures; {audit['invalid_final']} ultimately strict-invalid jobs. {audit['prompt_tokens']:,} input tokens and {audit['completion_tokens']:,} output tokens reported. {audit['reasoning_tokens']} reasoning tokens reported. {audit['unique_response_ids']} unique response IDs. Failed preflights are excluded from study metrics but included in the budget.",
              "",f"Reasoning was requested disabled, but {audit['nonzero_reasoning_responses']} responses reported nonzero reasoning tokens. This is logged rather than assumed to be a genuinely zero-thinking condition. Original compliance outcomes remain unchanged in the raw audit.",
              "","## What to do next","","Review decision frames and summaries before enlarging the sample. Revise ambiguous or overlapping action packages (especially Enemies and Postmaster); recruit independent readers to judge whether the richness arms preserve the same decision facts. Then test new, less recognizable stories with multiple independently written summaries/paraphrases, and a factual-detail-matched short control. A separate name-masked or genuinely unpublished-story condition is needed to test whether author recall drives any apparent gain. Do not publish a moral ranking from this pilot.",""]
    (run/"assessment.md").write_text("\n".join(lines))

    # Self-contained, offline HTML: every context and every parsed justification
    # is available without a server or external scripts/assets.
    esc=html.escape
    overview=[]
    for m in models:
        rr=[matched_stats[m][c] for c in ("R0","R1","R2")]
        overview.append("<tr><th>"+esc(NAMES[m])+"</th>"+"".join(f"<td>{pct(r['repeat_agreement'])}</td>" for r in rr)+"</tr>")
    sections=[]
    for item in items:
        id_=item["id"]
        frame=f"<p>{esc(item['forced_question'])}</p><ol type='A'>"+"".join(f"<li>{esc(v)}</li>" for v in item["options"].values())+"</ol>"
        arms=[]
        for c,text in pilot.contexts(item).items():
            arms.append(f"<details><summary>{c} context · {len(text.split()):,} words</summary><pre>{esc(text)}</pre></details>")
        evidence=[]
        for m in models:
            rows=[]
            ss=sorted([s for s in decisions if s["item"]==id_ and s["model"]==m],key=lambda s:(s["condition"],s["perturbation"],s["sample"]))
            for s in ss:
                rows.append(f"<tr><td>{s['condition']}/{s['perturbation']}/{s['sample']+1}</td><td>{s['canonical_choice']}</td><td>{s['parsed']['confidence']:.2f}</td><td>{esc(s['parsed']['reason'])}</td></tr>")
            recalls=[s for s in samples if s["item"]==id_ and s["model"]==m and s["kind"]=="recall"]
            recall=" ".join(esc(json.dumps(s.get("parsed",{}),ensure_ascii=False)) for s in recalls)
            if recall_coding:
                coding=recall_coding["items"][id_]
                matched_core=coding["matches_core_in_model_order"][recall_coding["model_order"].index(m)]
                recall+=f"<br><strong>Source-reviewed broad action match: {matched_core}.</strong> "+esc(coding["notes"])
            evidence.append(f"<details><summary>{esc(NAMES[m])} · {len(ss)} decisions</summary><p class='muted'>Separate author-recall probe: {recall}</p><div class='scroll'><table><thead><tr><th>Arm / prompt / sample</th><th>Semantic choice</th><th>Confidence</th><th>Justification</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>")
        sections.append(f"<section id='{id_}'><h2>{esc(item['title'])}</h2><p class='eyebrow'>{id_} · {esc(item['author'])} · {item['word_count']:,} words</p>{frame}<p class='muted'>Flags: {esc(', '.join(item['flags']) or 'none assigned')}<br>Author path (scoring annotation, never sent in decisions): {esc(item['author_path'] or 'Unavailable')}</p>{''.join(arms)}{''.join(evidence)}</section>")
    svg1=(run/"stability.svg").read_text();svg1=svg1[svg1.index("<svg"):]
    svg2=(run/"item_changes.svg").read_text();svg2=svg2[svg2.index("<svg"):]
    nav=" · ".join(f"<a href='#{i['id']}'>{esc(i['id'])}</a>" for i in items)
    html_doc=f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Does richer context steady the compass?</title>
<style>body{{margin:0;background:#f7f5ee;color:#292d28;font:17px/1.65 system-ui,sans-serif}}main{{max-width:1120px;margin:auto;padding:40px 24px}}h1{{font:clamp(2.3rem,5vw,4.3rem)/1.08 Georgia,serif;max-width:850px;font-weight:400}}h2{{font:2rem/1.2 Georgia,serif}}h3{{font-weight:550}}p{{max-width:850px}}a{{color:#376b68}}.eyebrow{{text-transform:uppercase;letter-spacing:.13em;font-size:12px}}.muted{{color:#61675e;font-size:14px}}.notice{{border-left:3px solid #b56944;padding:10px 20px;background:#ede9df}}section{{padding:35px 0;border-top:1px solid #d2d4c8;margin-top:35px}}table{{border-collapse:collapse;width:100%;font-size:14px;text-align:left}}th,td{{padding:10px 12px;border-bottom:1px solid #d9dacf;vertical-align:top}}th{{font-weight:600}}.scroll{{overflow:auto}}details{{padding:14px 0;border-bottom:1px solid #d9dacf}}summary{{cursor:pointer;color:#376b68;font-weight:550}}pre{{font:14px/1.7 system-ui;white-space:pre-wrap;max-height:600px;overflow:auto;background:#eeece4;padding:20px}}svg{{width:100%;height:auto}}nav{{position:sticky;top:0;padding:12px;background:#f7f5eef2;border-bottom:1px solid #d9dacf;z-index:2}}li{{margin-bottom:9px}}@media(max-width:650px){{main{{padding:24px 14px}}td,th{{padding:8px}}}}
</style><main><p class="eyebrow">Spinning Arrow · Private methods pilot · {esc(status['state'])}</p><h1>Does richer context steady the compass?</h1><p>A model can pick a different action when the same dilemma is phrased differently. We tested whether a fuller story makes those choices more repeatable.</p><p><strong>{len(decisions):,} decisions · 8 stories · 4 small models · ${status['budget']['actual']:.2f} total</strong></p><p class="notice">Not a moral scoreboard. More consistency does not mean a better decision. This small, selected sample cannot establish real-world moral reliability, and story memory remains a confound.</p>
<nav>Jump to story evidence: {nav}</nav><h2>Same five stories, three levels of context</h2><p>These plots compare only the five stories eligible for all three arms. Each prompt was repeated six times. Every displayed option is mapped back to its original meaning before scoring.</p><p class="notice">Format-robust analysis: plots use the first schema-valid choice even if its explanation exceeds 60 words. {audit['first_attempt_word_limit_failures']} first responses exceeded that limit. Original strict-format results and the selectively complete strict panel remain available in the assessment; no responses were silently shortened or replaced.</p>{svg1}<div class="scroll"><table><thead><tr><th>Repeat agreement</th><th>Short</th><th>Synopsis</th><th>Full text</th></tr></thead><tbody>{''.join(overview)}</tbody></table></div><p class="muted">Repeat agreement compares pairs of answers to exactly the same prompt. Flip rate compares modal answers after wording/order changes; ties are excluded. Complete denominators and tie bounds are in the accompanying summary and analysis files.</p>
<h2>Does the effect depend on the story?</h2><p>Green means full context produced more repeatable responses than the short vignette; brown means less repeatable. These are percentage-point changes, not moral scores.</p>{svg2}<h2>What this cannot tell us</h2><p>Longer text adds facts, atmosphere, and the character's previous choices. It may help a model understand the situation—or imitate a remembered story. The test cannot yet separate those explanations. Five full-text stories are too few for broad claims. The two preassigned blocks are repeated samples, not independent story replications.</p><p><a href="interpretation.md">Bottom line and examples</a> · <a href="assessment.md">Read the assessment</a> · <a href="summary.md">Strict metric table</a> · <a href="first_attempt_choice_valid/results.csv">Plotted results CSV</a> · <a href="analysis.json">Additional sensitivity metrics</a></p>{''.join(sections)}<footer><p class="muted">Local review artifact. No production deployment. Every story excerpt stops at the recorded source anchor; annotations containing author paths are never included in decision prompts.</p></footer></main></html>"""
    (run/"review.html").write_text(html_doc)
    print(json.dumps(dict(audit=audit,matched=matched_stats,delta=analysis['story_clustered_mean_delta'],range=analysis['story_cluster_bootstrap_95']),indent=2))

if __name__=="__main__":main()
