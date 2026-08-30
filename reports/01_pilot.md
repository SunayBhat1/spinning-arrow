# Phase 1 pilot report

**Run:** `20260830T060547Z__pilot__3258fb`  
**Window:** 2026-08-30T06:05:47Z to 2026-08-30T06:18:16Z  
**Raw data:** `data/raw/20260830T060547Z__pilot__3258fb/`  
**Manifest:** `data/manifests/20260830T060547Z__pilot__3258fb.json`  
**Records:** 2400 (400 per model)

The two documented mandatory-reasoning exceptions are pilot-only. Their reasoning tokens are retained in raw records and their results do not alter the Phase 2+ main-battery rule.

## 1. Parse rate

Clean parse rate is `answered / all calls`; it counts neither refusals nor malformed output as a usable response. The pre-specified scaling threshold is approximately 95%.

| Model | Answered | Refused | Hedged | Unparseable | Error | Clean parse rate |
|---|---:|---:|---:|---:|---:|---:|
| openai/gpt-oss-120b | 261 | 0 | 0 | 10 | 129 | 65.2% |
| google/gemini-3.5-flash-lite | 274 | 60 | 3 | 63 | 0 | 68.5% |
| mistralai/mistral-medium-3.1 | 400 | 0 | 0 | 0 | 0 | 100.0% |
| qwen/qwen3.8-27b | 400 | 0 | 0 | 0 | 0 | 100.0% |
| meta-llama/llama-3.3-70b-instruct | 392 | 0 | 0 | 8 | 0 | 98.0% |
| anthropic/claude-sonnet-5 | 400 | 0 | 0 | 0 | 0 | 100.0% |

## 2. Refusal rate by model and instrument

| Model | MFQ-2 refusals | ETHICS refusals | Overall refusals |
|---|---:|---:|---:|
| openai/gpt-oss-120b | 0.0% | 0.0% | 0.0% |
| google/gemini-3.5-flash-lite | 30.0% | 0.0% | 15.0% |
| mistralai/mistral-medium-3.1 | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.3-70b-instruct | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | 0.0% | 0.0% | 0.0% |

## 3. Position-bias magnitude

For each instrument, this is the range of mean selected *canonical option values* conditional on the displayed response letter. A value near zero indicates the display slot did not move answers; values are not compared across the two instruments' different scales.

| Model | Instrument | Valid n | A mean | B mean | C mean | D mean | E mean | Slot range |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| openai/gpt-oss-120b | mfq2 | 166 | 4.11 | 3.88 | 4.30 | 3.68 | 2.50 | 1.80 |
| openai/gpt-oss-120b | ethics_deontology | 95 | 0.49 | 0.50 | — | — | — | 0.01 |
| google/gemini-3.5-flash-lite | mfq2 | 77 | 3.78 | 4.33 | 3.31 | 1.00 | 1.94 | 3.33 |
| google/gemini-3.5-flash-lite | ethics_deontology | 197 | 0.46 | 0.41 | — | — | — | 0.05 |
| mistralai/mistral-medium-3.1 | mfq2 | 200 | 4.84 | 4.15 | 3.77 | 3.19 | 3.51 | 1.65 |
| mistralai/mistral-medium-3.1 | ethics_deontology | 200 | 0.28 | 0.30 | — | — | — | 0.02 |
| qwen/qwen3.8-27b | mfq2 | 200 | 3.16 | 3.26 | 2.82 | 1.52 | 2.23 | 1.74 |
| qwen/qwen3.8-27b | ethics_deontology | 200 | 0.25 | 0.26 | — | — | — | 0.01 |
| meta-llama/llama-3.3-70b-instruct | mfq2 | 192 | 4.32 | 4.12 | 3.89 | 2.21 | 3.60 | 2.11 |
| meta-llama/llama-3.3-70b-instruct | ethics_deontology | 200 | 0.12 | 0.17 | — | — | — | 0.05 |
| anthropic/claude-sonnet-5 | mfq2 | 200 | 3.29 | 3.20 | 3.23 | 2.25 | 3.05 | 1.03 |
| anthropic/claude-sonnet-5 | ethics_deontology | 200 | 0.43 | 0.40 | — | — | — | 0.03 |

## 4. Framing sensitivity

Pairs hold model, item, condition, and option permutation constant. The reported difference is `first-person mean − third-person mean` in the instrument's response-value units.

| Model | Instrument | Complete pairs | First-person mean | Third-person mean | Difference |
|---|---|---:|---:|---:|---:|
| openai/gpt-oss-120b | mfq2 | 66 | 3.97 | 4.08 | -0.11 |
| openai/gpt-oss-120b | ethics_deontology | 28 | 0.46 | 0.50 | -0.04 |
| google/gemini-3.5-flash-lite | mfq2 | 17 | 2.41 | 2.82 | -0.41 |
| google/gemini-3.5-flash-lite | ethics_deontology | 97 | 0.47 | 0.41 | 0.06 |
| mistralai/mistral-medium-3.1 | mfq2 | 100 | 3.72 | 3.84 | -0.12 |
| mistralai/mistral-medium-3.1 | ethics_deontology | 100 | 0.26 | 0.32 | -0.06 |
| qwen/qwen3.8-27b | mfq2 | 100 | 2.37 | 2.81 | -0.44 |
| qwen/qwen3.8-27b | ethics_deontology | 100 | 0.29 | 0.22 | 0.07 |
| meta-llama/llama-3.3-70b-instruct | mfq2 | 92 | 3.20 | 4.25 | -1.05 |
| meta-llama/llama-3.3-70b-instruct | ethics_deontology | 100 | 0.13 | 0.17 | -0.04 |
| anthropic/claude-sonnet-5 | mfq2 | 100 | 2.57 | 3.32 | -0.75 |
| anthropic/claude-sonnet-5 | ethics_deontology | 100 | 0.44 | 0.38 | 0.06 |

## 5. Fragility signal

For each model/instrument/item/framing cell, compute the population SD of selected response values across its five option permutations, then average those SDs. This is a descriptive pre-scoring fragility proxy, not an uncertainty interval.

| Model | Instrument | Cells with 2+ valid permutations | Mean within-cell SD | Max within-cell SD |
|---|---|---:|---:|---:|
| openai/gpt-oss-120b | mfq2 | 40 | 0.74 | 1.64 |
| openai/gpt-oss-120b | ethics_deontology | 25 | 0.02 | 0.50 |
| google/gemini-3.5-flash-lite | mfq2 | 20 | 0.10 | 1.50 |
| google/gemini-3.5-flash-lite | ethics_deontology | 40 | 0.10 | 0.49 |
| mistralai/mistral-medium-3.1 | mfq2 | 40 | 0.42 | 1.36 |
| mistralai/mistral-medium-3.1 | ethics_deontology | 40 | 0.10 | 0.49 |
| qwen/qwen3.8-27b | mfq2 | 40 | 0.45 | 1.60 |
| qwen/qwen3.8-27b | ethics_deontology | 40 | 0.14 | 0.49 |
| meta-llama/llama-3.3-70b-instruct | mfq2 | 40 | 0.55 | 1.66 |
| meta-llama/llama-3.3-70b-instruct | ethics_deontology | 40 | 0.07 | 0.49 |
| anthropic/claude-sonnet-5 | mfq2 | 40 | 0.35 | 1.20 |
| anthropic/claude-sonnet-5 | ethics_deontology | 40 | 0.11 | 0.49 |

## 6. Cost reconciliation

Forecast is a conservative, pre-run ceiling calculation: 180 input tokens plus each model's recorded `max_tokens`, priced at the frozen per-million rates for 400 calls. Actual is the sum of OpenRouter `usage.cost` values in the raw records and must be reconciled with the OpenRouter dashboard before approving Gate 1.

| Model | Forecast (USD) | Actual (USD) | Actual / forecast |
|---|---:|---:|---:|
| openai/gpt-oss-120b | $0.007016 | $0.009776 | 1.393 |
| google/gemini-3.5-flash-lite | $0.533600 | $0.033165 | 0.062 |
| mistralai/mistral-medium-3.1 | $0.035200 | $0.013220 | 0.376 |
| qwen/qwen3.8-27b | $0.038760 | $0.014574 | 0.376 |
| meta-llama/llama-3.3-70b-instruct | $0.053392 | $0.006266 | 0.117 |
| anthropic/claude-sonnet-5 | $0.176000 | $0.098700 | 0.561 |
| **Total** | **$0.843968** | **$0.175701** | **0.208** |

## 7. Latency, error, and rate-limit observations

Latency includes each completed client call. Error rates include transport, accounting, and contentless-completion errors; provider retryable HTTP statuses are retried up to three times.

| Model | Mean latency (ms) | P95 latency (ms) | Error rate | 429/rate-limit errors |
|---|---:|---:|---:|---:|
| openai/gpt-oss-120b | 1685 | 5880 | 32.2% | 0 |
| google/gemini-3.5-flash-lite | 944 | 1869 | 0.0% | 0 |
| mistralai/mistral-medium-3.1 | 846 | 2452 | 0.0% | 0 |
| qwen/qwen3.8-27b | 835 | 2721 | 0.0% | 0 |
| meta-llama/llama-3.3-70b-instruct | 902 | 2864 | 0.0% | 0 |
| anthropic/claude-sonnet-5 | 2259 | 2923 | 0.0% | 0 |

## Recommendation and surprises

Do not scale this six-model configuration to Phase 2 unchanged. The two low-parse mandatory-reasoning exceptions are ineligible for the D5 main battery; the strict-D5 models at or above the parse threshold are the candidate subset for Gate 1 review.

**Surprises to review:** below-95% parse: openai/gpt-oss-120b, google/gemini-3.5-flash-lite; 129 explicit error records.

Gate 1 remains a Sunay decision. This report deliberately does not advance the project to Phase 2 on its own.
