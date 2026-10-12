# Eight-story smoke selection

Selected before observing study results. Two protocol frames, three batch A frames, three batch B frames; eight different authors. No paid generation was used to write summaries. All summaries and question paraphrases are frozen, human-reviewable files.

| ID | Work | Why include it | Measured whole-story words | Pre-stop words | Arms |
|---|---|---|---:|---:|---|
| N04 | Jekyll and Hyde | Requested original; responsibility/control conflict. Famous-work recall stress case. | 25,631 | 6,653 | R0, R1 |
| N07 | Bartleby | Requested original; care, agency, and limits of obligation. | 14,358 | 11,176 | R0, R1 |
| A04 | The Minister's Black Veil | Private conviction versus intimacy; explicit final request before an answer. | 5,150 | 3,346 | R0, R1, R2 |
| A14 | To Build a Fire | Immediate survival versus harming an animal; physical constraints enrich the fork. | 7,085 | 5,416 | R0, R1, R2 |
| A25 | The Three Strangers | Loyalty to a brother versus law and personal exposure; clear recognition point. | 8,308 | 5,354 | R0, R1 |
| B02 | Enemies | Professional obligation versus acute family grief; uncertain secondhand emergency. | 5,429 | 2,121 | R0, R1, R2 |
| B06 | God Sees the Truth, but Does Not Tell at Once | Truth, retaliation, mercy, and uncertainty about guilt. | 3,147 | 2,710 | R0, R1, R2 |
| B21 | The Postmaster | Informal care and attachment versus the boundaries of responsibility. | 2,195 | 1,551 | R0, R1, R2 |

R2 eligibility uses the **whole story**, not just the shorter excerpt, following the updated instruction. A25's supplied 8,000-word estimate measured 8,308, so its full-text arm is omitted. The three-arm comparison therefore uses the same five stories, never all eight R0 items against only five R2 items. R0–R1 may additionally be compared on all eight.

## Source and frame checks

- Jekyll: the original frame incorrectly asserts amnesia and full control. Those assertions were removed. The cut is in the early linear Carew-murder scene, not in the retrospective confession that already reveals later outcomes. Identity/formula and the return to Jekyll are explicit shared frame premises. No offered action exactly matches the author's immediate combination of renunciation and retaining the formula; author-option match is unavailable, not coded B.
- Bartleby: cut after his three days of consideration and renewed refusal, before the lawyer's subsequent course.
- Minister: cut at Elizabeth's final request, before Hooper answers. His prior statements are retained as history, so R2 may favor continuity with the character's previous commitments. This is a confound, not a hidden success.
- Fire: cut at the remembered survival story, before the man announces his intended action toward the dog.
- Three Strangers: cut before the third visitor flees. His kinship and recognition are explicit frame knowledge because the narrator explains them later. R2 is not used.
- Enemies: cut at Abogin's promise of a one-hour return, before Kirilov's decision and before the visit's revelations. Some draft options have uneven feasibility: the story says no other doctor is nearby, and D ambiguously says “go” while requiring the patient to be brought here. Options are preserved from the supplied bank; interpret with this limitation.
- God Sees: the frame now says **suspects**, not knows, who committed the murder. It distinguishes that uncertainty from firsthand knowledge of tunnel digging. Exact story ends before “Hunting Worse Than Slavery”; the surrounding anthology is not counted as this story.
- Postmaster: he **resigns after a denied transfer**, rather than receiving a transfer. Cut before his reply to Ratan. Canon B is approximate: later actions also overlap C. Do not use author match as a quality measure.

## Bank and rights

`raw/` preserves all four supplied files verbatim. `item_bank.jsonl` retains all 60 frames, including excluded records for traceability. Unverified anchors are null, not invented from descriptive stopping points. `normalization_log.md` records mappings and corrections. `source_inventory.json` records attempted batch-A extraction; network failures, missing boundaries, and >12k-word candidates are excluded from selection. Heuristic unselected counts are labeled unverified and are **not** used in prompts.

Animal Farm and Of Mice and Men are excluded for US copyright. The PG5200 Metamorphosis source is also excluded: its David Wyllie translation is copyrighted even though Kafka's German original is public domain. The unused cached translation has been removed from this branch (recoverable in its earlier commit).

The selected English originals predate 1930. The translations used are Constance Garnett's Chekhov (PG13412), Leo Wiener's Tolstoy (PG38025), and the uncredited English text in Macmillan's 1918 Stories from Tagore (PG33525). This is a US-public-domain scope, not a worldwide rights opinion. Source URLs, source hashes, exact matched anchor text, and Unicode character offsets are in `texts/*.metadata.json`.

The Lady, or the Tiger? remains in the bank with `no_author_path`. Required high-contamination flags are assigned independently of selection. Lesser-known selected stories can also be memorized; absence of that flag does not certify novelty.

## Fixed run plan

Four inexpensive models: GPT-4o mini, GPT-4.1 mini, Gemini 2.5 Flash-Lite, Claude Haiku 4.5. Six independent responses for each of four perturbations per eligible context. Sample indices 0–2 and 3–5 form two preassigned repeat blocks, analyzed separately as a sensitivity check. The blocks are interleaved in randomized dispatch order, not separate temporal replications.

This yields 21 item/context combinations × 4 perturbations × 6 samples × 4 models = **2,016 decisions**, plus 32 separate no-story-excerpt recall checks. There is no outcome-adaptive stopping or extension to seek a favorable richness effect. The $5 ceiling includes failed probes and format retries. Stop once this balanced design is complete; spending the entire allowance is not itself an experimental objective.

An initial format probe produced option text instead of a one-character label twice ($0.0002367). A second preflight passed three models but Haiku returned Markdown-fenced JSON twice. Both preflights are retained and excluded from study metrics; combined spend was $0.00277425. The instruction was clarified and provider-enforced JSON Schema enabled before the full study. All final study cells use that same format.

During collection, length-only validation failures were observed, concentrated in Haiku. Before looking at aggregate decisions, a first-attempt choice-valid sensitivity analysis was added to avoid silently substituting a retry's choice merely because it had a shorter explanation. This does not change the fixed sample plan or erase strict-format failures. Both analyses and their denominators are retained.
