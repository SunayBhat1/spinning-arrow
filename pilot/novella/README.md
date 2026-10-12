# Does narrative context stabilize a model's decision?

A private, exploratory **methods pilot**, not a moral scoreboard. It asks whether a model makes the same forced decision more consistently when it receives a longer account of the situation. Stability does not establish correctness, desirable values, or reliable behavior in a real agent workflow.

Completed run: [plain-language interpretation](runs/20261012T054221157187Z/interpretation.md), [review page with plots and every response](runs/20261012T054221157187Z/review.html), [full assessment](runs/20261012T054221157187Z/assessment.md). Actual cumulative inference spend: **$2.02427972**. The result is mixed: richer context did not uniformly increase stability. These links refer to a completed private methods pilot, not a production website update.

The expanded design uses **eight stories, four small models, and six independent responses per prompt cell**. Five stories have all three context arms; three exceed the user's whole-story 8,000-word R2 limit and have R0/R1 only. Selection, source corrections, and caveats are in [items/smoke_selection.md](items/smoke_selection.md).

## What is held fixed and what varies?

- R0: frozen neutral vignette, 80–120 words.
- R1: frozen neutral synopsis, 600–800 words.
- R2: actual public-domain story text through a verified anchor, only for stories under 8,000 words. A 25,000-token contingency retains the opening 3,000 and last 20,000 pre-stop tokens; none of the selected excerpts needs it.
- Each arm ends with the same second-person question and the same action options. p0 is canonical, p1 reorders and relabels options using a fixed seed, p2 substitutes a saved question paraphrase, and p3 uses numeric labels. Scoring maps displayed labels back to semantic options.
- Each cell has six independently sampled answers at temperature 0.7, with a 300-token output cap. No generation seed is reused. Reasoning is disabled where supported. Provider is pinned with no fallback. OpenRouter response caching is explicitly disabled; ordinary prompt-token caching may reduce cost without reusing answers.
- p4 is a separate literary-knowledge probe with a title/author and decision cue, but no story excerpt, options, or answer annotation. It is not counted as a decision perturbation.
- Provider-enforced JSON Schema requires choice, confidence, and a justification. The prompt additionally requires at most 60 words. Invalid output gets one retry with the same prompt; both attempts count toward spending and are retained. Transport/unknown-billing failures halt, without a speculative retry.

The six samples are preassigned to two blocks of three for a split-half check. They are interleaved during dispatch; this is not a later-date replication. Do not add samples selectively in response to interesting results.

## Preparation and provenance

`items/raw/` contains the four supplied batch files unchanged. `items/item_bank.jsonl` normalizes all 60 source frames, retaining excluded records with explicit flags. Only the eight validated records in `items.json` are executable. Unknown metadata stays null or flagged. The remaining bank is **not fully validated for execution**.

`prepare_bank.py` strips Gutenberg wrappers, extracts selected stories from collections, checks unique exact anchors allowing line wraps, and records measured words, hashes, and exclusive character offsets. Full downloads stay in an external temporary cache; repository text caches contain only pre-stop excerpts. R1 summaries and question paraphrases were written once by the coding assistant, not by a paid model call. Review them as authored measurement instruments, not neutral ground truth.

Animal Farm and Of Mice and Men are excluded. The former draft's PG5200 Metamorphosis translation was found to be copyrighted and removed. Selected translated editions predate 1930; this pilot uses a US rights scope. Prior failed/no-key preparation runs remain for audit and are not evidence.

```sh
python3 pilot/novella/prepare_bank.py --scan-batch-a
```

## Run safely

The runner uses **OPENROUTER_API_KEY**, either from the process environment or an explicitly supplied local env file. It does not print or save credentials. The existing project key can fund all four selected models; missing direct OpenAI/Anthropic keys do not prevent OpenRouter use. If the OpenRouter key is missing, the provider is skipped and logged.

```sh
UV_CACHE_DIR=/private/tmp/spinning-arrow-uv-cache \
  uv run --no-project --with-requirements pilot/novella/requirements.txt \
  pilot/novella/run_pilot.py --dry-run --n 6

UV_CACHE_DIR=/private/tmp/spinning-arrow-uv-cache \
  uv run --no-project --with-requirements pilot/novella/requirements.txt \
  pilot/novella/run_pilot.py --yes --n 6 --env-file .env
```

CLI controls include `--models` (comma-separated reviewed OpenRouter IDs), `--items` (IDs or slugs), `--n`, `--workers` (1–8), `--seed`, `--probe-only`, and `--resume runs/path`. `--resume` verifies prompt hashes and retains the original plan and provider prices; it does not silently mix changed prompts. Failed/invalid completed samples are not silently replaced on resume.

Live provider prices are saved in the manifest. The dry-run table uses tiktoken with framing overhead and a 15% margin (an approximation for non-OpenAI tokenizers), assuming every completion reaches 300 tokens. Above $4 it drops the longest R2 arm first, then reduces n to 2. It reports the separate every-request retry stress case too. Normal execution pauses for confirmation unless `--yes` is supplied.

**The shared $5 guard includes every run and retry in `runs/budget_ledger.jsonl`. Do not delete/reset it to continue this authorization.** Each request reserves a conservative byte-based input bound and maximum output cost before dispatch. API-side maximum prices and provider pinning prevent costlier fallback routing. Known cost comes from `usage.cost`; unknown charges retain their reservation and stop further work pending reconciliation. Parallel workers and separate processes share the ledger lock. The ceiling concerns API inference charges, not unrelated account use or prior credit-purchase fees.

## Review the outputs

Every run directory records the full plan, price snapshot, prompt hashes, key-free request/response JSONL, validated samples, failures, spend, and completion state. `results.csv` and `summary.md` provide item/model/context metrics:

- Modal option and its share across all valid samples and perturbations.
- Flip rate: fraction of unique p1–p3 modes differing from the unique p0 mode. Ties and incomplete cells are excluded with explicit denominators, never broken alphabetically.
- Mean within-cell entropy (bits) and pairwise repeat agreement. A unanimous six-response cell has 100% pairwise agreement; greater entropy means more spread.
- Mean self-reported confidence (not a calibration score).
- Descriptive author-path match when an unambiguous mapping exists. Jekyll has no exact mapping; Postmaster overlaps B/C and is approximate.

Use a matched five-story panel to compare R0/R1/R2. Compare R0/R1 on all eight separately. More tokens can change the facts, emotional framing, and visible prior commitments; this experiment cannot attribute a change to length alone. There is no name masking, and recall probes cannot prove whether a model relied on memory. A small, selected set of stories and repeated samples do not constitute broad statistical generalization.

`analyze.py <run-directory>` rebuilds `assessment.md`, scientific plots, and a self-contained `review.html` with all contexts, options, and justifications. It also writes an explicitly labeled **first-attempt choice-valid sensitivity analysis** under `first_attempt_choice_valid/`. This retains schema-valid first choices whose justifications exceeded 60 words, so a retry's different sampled choice cannot silently substitute for them. The original strict results remain intact. This additional analysis was motivated by observed format failures before examining aggregate choice outcomes, not preregistered in the original protocol. Strict comparisons use only stories complete in all three arms for a given model and show the resulting smaller denominator.

## Offline checks

```sh
UV_CACHE_DIR=/private/tmp/spinning-arrow-uv-cache \
  uv run --no-project --with-requirements pilot/novella/requirements.txt \
  python -m unittest discover -s pilot/novella -p 'test_*.py' -v
```

Tests cover exclusive cuts, prompt lengths, option mappings, ties, strict responses, copyright flags, durable reservations, retry headroom, and missing usage. Existing September pilot data and the production website are out of scope. Work remains on the draft pilot branch; do not merge or publish claims from these results.
