"""Normalize the supplied frames and reproducibly validate/cut source texts.

Full Gutenberg downloads live outside the repository. Only pre-decision excerpts
are saved here. No generation API is used in preparation.
"""
import argparse
import hashlib
import json
import re
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROTOCOL = ROOT.parents[1] / "docs/NOVELLA_PILOT_PROTOCOL.md"
SELECTED = {
    "N04": ("jekyll_hyde", 43, None, None, "At the horror of these sights and sounds, the maid fainted.", None),
    "N07": ("bartleby", 11231, None, None, "But having taken three days to meditate upon it, he apprised me that his original determination remained the same; in short, that he still preferred to abide with me.", "B"),
    "A04": ("minister_veil", 13707, "THE MINISTER’S BLACK VEIL", "THE MAYPOLE OF MERRY MOUNT", "“Lift the veil but once and look me in the face,” said she.", "A"),
    "A14": ("build_fire", 2429, "TO BUILD A FIRE", "THAT SPOT", "He remembered the tale of the man, caught in a blizzard, who killed a steer and crawled inside the carcass, and so was saved.", "A"),
    "A25": ("three_strangers", 3056, "THE THREE STRANGERS", "THE WITHERED ARM", "his white lips were parted, and his eyes fixed on the merry officer of justice in the middle of the room.", "A"),
    "B02": ("enemies", 13412, "ENEMIES", "THE EXAMINING MAGISTRATE", "Only one hour.", "A"),
    "B06": ("god_sees_truth", 38025, "GOD SEES THE TRUTH, BUT DOES NOT TELL AT ONCE", "HUNTING WORSE THAN SLAVERY", "Who has been digging it?", "B"),
    "B21": ("postmaster", 33525, "THE POSTMASTER", "WORDS TO BE STUDIED", '"Dada, will you take me to your home?"', "B"),
}
QUESTIONS = {
    "N04": "You are Dr. Jekyll. Hyde, the identity produced by your formula, has just killed a man in the street. For this decision, you are back in your own form, horrified; the formula remains available and your connection to Hyde is secret. What do you do now?",
    "N07": "You are the Lawyer. Bartleby has stopped working, lives in your office, and has again refused to leave. You have offered money and tried persuasion; you know of no family who can take him in. His presence is disrupting your practice. What do you do now?",
    "A04": "You are the Reverend Mr. Hooper. Elizabeth, your fiancée, asks you to lift your black veil once so she can see your face. You have kept its meaning private and said it must remain. She is prepared to leave if you refuse. What do you do now?",
    "A14": "You are the man on the Yukon trail. Your fire has failed, your hands are frozen, and your dog is beside you. You recall someone surviving a blizzard inside a freshly killed animal. You have a knife, but little use of your fingers. What do you do now?",
    "A25": "You are the third stranger. You enter a shepherd's party on your way to visit your condemned brother in prison. You recognize your brother, escaped and sitting by the chimney, and the other stranger is singing about hanging a sheep-stealer tomorrow. He is your brother's intended executioner. Neither has identified you to the company. What do you do now?",
    "B02": "You are Dr. Kirilov. Your only child has just died and your wife is alone with his body. Abogin says his wife has suddenly become gravely ill, eight or nine miles away, and promises to bring you home within an hour. You have explained your loss, but he continues to plead for your help. What do you do now?",
    "B06": "You are Aksénov. You have spent twenty-six years in prison for a murder you did not commit. You strongly suspect Makar committed it, but are not certain. You did see him digging an escape tunnel; he threatened you if you told. The prison chief now demands that you identify the digger, who will be severely flogged. What do you do now?",
    "B21": "You are the postmaster. After your request for a transfer was refused, you resigned and told Ratan you are going home. This orphan girl has cared for you during illness, and you have taught her to read. She now asks whether you will take her home with you. What do you do now?",
}
HIGH_RISK = {"A05", "A06", "A07", "B12", "B19", "B20", "B23", "N04"}
PG_ORIGINAL = {"N04":43, "N05":219, "N06":209, "N07":11231, "N08":689, "N09":1952, "N10":4517}

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()).strip()

def strip_wrapper(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    start = re.search(r"\*\*\* START OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", text, re.I)
    end = re.search(r"\*\*\* END OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", text, re.I)
    if not start or not end:
        raise ValueError("Missing Gutenberg wrapper; refuse unverified extraction")
    return text[start.end():end.start()].strip()

def headings(text, heading):
    return [m for m in re.finditer(r"(?m)^[^\n]+$", text)
            if norm(m.group()) == norm(heading)]

def extract(text, title, next_title=None):
    if title is None:
        return text, 0, len(text)
    matches = headings(text, title)
    # Contents entries cluster early; choose the last title before a substantial
    # prose block. This also skips duplicated chapter title pages.
    candidates = []
    for m in matches:
        tail = text[m.end():m.end()+1500]
        if len(re.findall(r"[.!?][\"’”]?\s", tail)) >= 4:
            candidates.append(m)
    if not candidates:
        raise ValueError("No verified story heading followed by prose")
    start = candidates[-1].start()
    if next_title:
        ends = [m.start() for m in headings(text, next_title) if m.start() > start]
        if not ends:
            raise ValueError("Next story boundary not found")
        end = min(ends)
    else:
        # Generic inventory: next all-caps heading with following prose, not a
        # roman-numeral subsection. Results are explicitly heuristic/unverified.
        candidates_end = []
        for m in re.finditer(r"(?m)^\s*([A-Z][A-Z ’'—,?!:;().-]{6,})\s*$", text[start+len(title):]):
            pos = start+len(title)+m.start()
            if len(m.group(1).split()) >= 2 and pos > start+1000:
                candidates_end.append(pos)
        end = min(candidates_end) if candidates_end else len(text)
    return text[start:end].strip(), start, end

def anchor_cut(text, anchor):
    # re.escape uses '\\ ' for spaces; allow Gutenberg's line wrapping.
    pattern = re.escape(anchor).replace("\\ ", r"\s+")
    matches = list(re.finditer(pattern, text))
    if len(matches) != 1:
        raise ValueError(f"Anchor must occur once, found {len(matches)}: {anchor}")
    m = matches[0]
    return text[:m.end()], m.start(), m.end(), m.group()

def download(pg, cache):
    path = cache / f"{pg}.txt"
    aliases = {43:"jekyll",11231:"bartleby"}
    if not path.exists() and pg in aliases and (cache / f"{aliases[pg]}.txt").exists():
        path = cache / f"{aliases[pg]}.txt"
    if not path.exists():
        req = urllib.request.Request(f"https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt", headers={"User-Agent":"spinning-arrow-methods-pilot/0.2"})
        path.write_bytes(urllib.request.urlopen(req, timeout=45).read())
    return path.read_text(encoding="utf-8-sig")

def normalize():
    log = []
    bank = []
    protocol = PROTOCOL.read_text()
    for match in re.finditer(r"(?ms)^### (\d+)\. (.*?) \(([^,]+), (\d+)\)(.*?)(?=^### \d+\.|^## Item construction rules)", protocol):
        number, title, author, year, body = match.groups()
        id_ = f"N{int(number):02}"
        def field(name):
            result = re.search(rf"\*\*{re.escape(name)}:\*\* (.*?)(?=\n\n|\Z)", body, re.S)
            return result.group(1).strip() if result else None
        options = dict(re.findall(r"^- \*\*([A-E])\.\*\* (.+)$", body, re.M))
        bank.append(dict(id=id_,title=title,author=author,year=int(year),translator=None,word_count=None,
                         source_url=f"https://www.gutenberg.org/ebooks/{PG_ORIGINAL[id_]}" if id_ in PG_ORIGINAL else None,
                         rights_status="excluded_US_copyright" if id_ in {"N01","N03"} else "source_rights_unverified",
                         plot=field("Story"),focal_character=field("Focal character"),stop_anchor=None,
                         forced_question=field("Forced question"),options=options,author_path=field("Author's path (for scorers)"),
                         tradeoff_axis=field("Dilemma"),flags=["stop_anchor_unverified"] + (["excluded"] if id_ in {"N01","N03"} else [])))
        log.append(f"{id_}: parsed protocol; year explicit. Gutenberg source mapping supplied during preparation, not in frame. Translator and measured word count unknown; descriptive stopping point is NOT an exact anchor.")
    for filename in ["batch_a.jsonl", "batch_b.jsonl"]:
        for line in (ROOT/"items/raw"/filename).read_text().splitlines():
            row = json.loads(line)
            bank.append(dict(id=row["id"], title=row["title"], author=row["author"],year=row["year"],translator=row.get("translator"),
                word_count=row.get("approx_words"),source_url=row["gutenberg_url"],rights_status="supplied_PD_claim_unverified",
                plot=row["plot"],focal_character=row["focal_character"],stop_anchor=None,forced_question=row["forced_question"],
                options=row["options"],author_path=row["author_path"],tradeoff_axis=row.get("tradeoff_axis",row.get("axis")),
                flags=["estimated_word_count","stop_anchor_unverified"]))
            log.append(f"{row['id']}: approx_words → word_count (estimate only); gutenberg_url → source_url; {'axis' if 'axis' in row else 'tradeoff_axis'} → tradeoff_axis. No exact stop anchor supplied. Translation/PD claims copied, not inferred. First-person draft question retained in bank unless selected; selected questions rewritten in second person.")
    assert len(bank) == 60, len(bank)
    for row in bank:
        if row["id"] in HIGH_RISK:
            row["flags"].append("high_contamination_risk")
        if row["id"] == "A23":
            row["flags"].append("no_author_path")
            row["author_path"] = None
        if row["id"] == "N02":
            row["rights_status"] = "excluded_selected_translation_copyrighted"
            row["flags"] += ["excluded", "PD_original_does_not_clear_translation"]
            log.append("N02: PG5200 David Wyllie translation is copyrighted; excluded source, not a claim that every translation is copyrighted.")
    return bank, log

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache",type=Path,default=Path("/private/tmp/novella-source-probe"))
    parser.add_argument("--scan-batch-a",action="store_true")
    args=parser.parse_args()
    args.cache.mkdir(parents=True,exist_ok=True)
    bank, log = normalize()
    manifest=[]
    inventory=[]
    for row in bank:
        id_=row["id"]
        if id_ not in SELECTED and not (args.scan_batch_a and id_.startswith("A")):
            continue
        try:
            pg=int(row["source_url"].rstrip("/").split("/")[-1])
            raw=download(pg,args.cache)
            text=strip_wrapper(raw)
            if id_ not in SELECTED:
                story, start, end=extract(text,row["title"])
                count=len(story.split())
                # Do not silently use heuristic cuts in paid prompts.
                status="dropped_over_12000_words" if count>12000 else "located_candidate_requires_boundary_and_stop_review"
                inventory.append(dict(id=id_,word_count=count,status=status,start=start,end=end,method="title/prose heuristic; not manually verified"))
                row["flags"].append(status)
                continue
            slug, pg, heading, next_heading, anchor, canon=SELECTED[id_]
            story,start,end=extract(text,heading,next_heading)
            count=len(story.split())
            if id_.startswith(("A","B")) and count>12000:
                raise ValueError(f"Selected story too long: {count} words")
            cut,a,b,exact=anchor_cut(story,anchor)
            (ROOT/"texts"/f"{slug}.up_to_stop.txt").write_text(cut)
            meta=dict(id=id_,slug=slug,source_url=f"https://www.gutenberg.org/cache/epub/{pg}/pg{pg}.txt",
                      source_sha256=hashlib.sha256(raw.encode()).hexdigest(),story_start_in_stripped_collection=start,
                      story_end_in_stripped_collection=end,measured_story_words=count,pre_stop_words=len(cut.split()),
                      anchor_sentence=anchor,exact_anchor_text=exact,anchor_start_in_story=a,stop_char_exclusive=b,
                      offset_convention="Unicode characters in LF-normalized, wrapper-stripped story; not UTF-8 byte offsets",
                      cut_sha256=hashlib.sha256(cut.encode()).hexdigest(),r2_eligible=count<8000)
            (ROOT/"texts"/f"{slug}.metadata.json").write_text(json.dumps(meta,indent=2,ensure_ascii=False)+"\n")
            row.update(word_count=count,stop_anchor=anchor,forced_question=QUESTIONS[id_],rights_status="US_public_domain_pre1930_source_edition")
            row["flags"]=[f for f in row["flags"] if f not in {"estimated_word_count","stop_anchor_unverified"}]
            if not meta["r2_eligible"]:
                row["flags"].append("R2_omitted_full_story_at_least_8000_words")
            if id_ in {"N04","A25"}:
                row["flags"].append("frame_supplies_private_knowledge_revealed_later_in_book")
            if id_=="N04":
                row["flags"].append("no_exact_author_option")
                row["author_path"]="After Carew's murder Jekyll resolves to renounce Hyde but retains the formula; later transformations become involuntary. No offered option exactly matches this immediate combination."
                log.append("N04: corrected amnesia/control assumptions; early linear cut before police investigation avoids retrospective ending. Return to Jekyll and identity/formula are an explicit shared frame premise. No exact author-option score (old B coding was not defensible).")
            if id_=="B06":
                log.append("B06: corrected knowledge of murderer's identity to strong suspicion; text explicitly preserves doubt.")
            if id_=="B21":
                row["plot"]="A lonely Calcutta postmaster in a remote village is cared for by the orphan Ratan. His request for a transfer is refused; he resigns and prepares to leave."
                log.append("B21: corrected successful transfer to rejected transfer followed by resignation. B is approximate canon: later actions also include asking his successor to care for Ratan (C).")
            manifest.append(dict(**row,slug=slug,author_choice=canon,metadata=meta))
            inventory.append(dict(id=id_,word_count=count,status="verified_selected",pre_stop_words=len(cut.split()),r2=meta["r2_eligible"]))
        except Exception as error:
            inventory.append(dict(id=id_,status="dropped_source_or_boundary_not_verified",reason=str(error)))
            row["flags"].append("source_or_boundary_not_verified")
            if id_ in SELECTED:
                print(json.dumps(inventory[-1]),flush=True)
    out=ROOT/"items"
    (out/"item_bank.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in bank))
    (out/"normalization_log.md").write_text("# Normalization and corrections\n\n"+"\n\n".join(log)+"\n")
    (out/"source_inventory.json").write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+"\n")
    (ROOT/"items.json").write_text(json.dumps(dict(schema_version=3,collection="novella-stability-smoke-v0.3",items=manifest),indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(inventory,indent=2,ensure_ascii=False))
    if len(manifest)!=8:
        raise SystemExit(f"Only {len(manifest)}/8 validated; no paid run permitted")

if __name__=="__main__":
    main()
