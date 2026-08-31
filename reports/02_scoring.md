# Cross-model main-battery report

**Run:** `20260831T055938Z__phase2__0dade8`
**Window:** 2026-08-31T07:10:29Z to 2026-08-31T08:56:03Z
**Commit:** `056962289d6e356775ebd82d1964f7100e347739`
**Raw data:** `data/raw/20260831T055938Z__phase2__0dade8/`
**Manifest:** `data/manifests/20260831T055938Z__phase2__0dade8.json`
**Derived data:** `data/derived/20260831T055938Z__phase2__0dade8/`

## Decision-ready result

This completed launch panel is mechanically reproducible. Every included model passed a format and zero-reasoning preflight before collection. Each score averages valid option permutations within an item/condition/framing cell. Cells below 70% valid coverage are suppressed; scale intervals use 2,000 deterministic item-and-permutation bootstraps.

## Run integrity and response quality

**Records:** 132,300 (6,300 per model)
**OpenRouter-recorded cost:** $6.604989
**Reasoning tokens in main battery:** 0 (hard requirement)

| Model | Parse | Attention | Refusal | Hedge | Unparseable | Error | Mean fragility | Suppressed cells | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| openai/gpt-5.4-mini | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.161 | 0 | $0.5979 |
| openai/gpt-5.6-luna | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.131 | 0 | $0.1552 |
| google/gemini-2.5-flash-lite | 95.9% | 100.0% | 0.0% | 0.0% | 4.1% | 0.0% | 0.121 | 59 | $0.0591 |
| google/gemini-2.5-flash | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.136 | 0 | $0.1833 |
| anthropic/claude-sonnet-5 | 99.8% | 100.0% | 0.0% | 0.0% | 0.2% | 0.0% | 0.116 | 2 | $1.9786 |
| x-ai/grok-4.20 | 95.5% | 100.0% | 0.0% | 0.0% | 4.5% | 0.0% | 0.190 | 86 | $0.8405 |
| meta-llama/llama-3.1-70b-instruct | 91.7% | 100.0% | 0.0% | 0.0% | 8.3% | 0.0% | 0.214 | 148 | $0.3387 |
| meta-llama/llama-3.1-8b-instruct | 98.8% | 96.7% | 0.7% | 0.0% | 0.5% | 0.0% | 0.195 | 19 | $0.0155 |
| mistralai/mistral-medium-3.1 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.104 | 0 | $0.2264 |
| mistralai/mistral-small-3.2-24b-instruct | 98.3% | 100.0% | 0.0% | 0.0% | 1.7% | 0.0% | 0.103 | 16 | $0.0458 |
| qwen/qwen3.8-27b | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.122 | 0 | $0.2927 |
| openai/gpt-4o-mini-2024-07-18 | 92.8% | 100.0% | 0.0% | 0.0% | 7.2% | 0.0% | 0.129 | 122 | $0.0935 |
| deepseek/deepseek-v4-pro-0813 | 95.9% | 100.0% | 0.0% | 0.0% | 4.1% | 0.0% | 0.200 | 46 | $0.7885 |
| deepseek/deepseek-v4-flash-0731 | 94.6% | 93.0% | 0.1% | 0.0% | 5.2% | 0.1% | 0.246 | 74 | $0.0431 |
| z-ai/glm-5.2 | 97.9% | 100.0% | 0.1% | 0.0% | 2.0% | 0.0% | 0.183 | 12 | $0.4048 |
| z-ai/glm-4.5-air | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.133 | 0 | $0.0693 |
| google/gemma-3-27b-it | 99.9% | 100.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.104 | 0 | $0.0635 |
| nvidia/nemotron-3.5-lightning | 99.9% | 100.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.198 | 1 | $0.0683 |
| amazon/nova-lite-v1 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.112 | 0 | $0.0356 |
| microsoft/phi-4 | 22.8% | 79.7% | 0.2% | 0.0% | 77.1% | 0.0% | 0.063 | 1089 | $0.0471 |
| openai/gpt-4.1-mini | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.107 | 1 | $0.2576 |

### Outcome classes by instrument

| Model | Instrument | Calls | Parse | Refusal | Hedge | Unparseable | Error |
|---|---|---:|---:|---:|---:|---:|---:|
| openai/gpt-5.4-mini | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.6-luna | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.6-luna | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.6-luna | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.6-luna | mfq2_phase2 | 720 | 99.9% | 0.0% | 0.0% | 0.0% | 0.1% |
| openai/gpt-5.6-luna | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash-lite | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash-lite | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | 2400 | 99.4% | 0.0% | 0.0% | 0.6% | 0.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | 720 | 77.6% | 0.0% | 0.0% | 22.4% | 0.0% |
| google/gemini-2.5-flash-lite | ous_ggb | 480 | 82.9% | 0.0% | 0.0% | 17.1% | 0.0% |
| google/gemini-2.5-flash | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash | mfq2_phase2 | 720 | 99.9% | 0.0% | 0.0% | 0.1% | 0.0% |
| google/gemini-2.5-flash | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | ipip_neo_120 | 2400 | 99.6% | 0.0% | 0.0% | 0.4% | 0.0% |
| anthropic/claude-sonnet-5 | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | ous_ggb | 480 | 99.2% | 0.0% | 0.0% | 0.8% | 0.0% |
| x-ai/grok-4.20 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| x-ai/grok-4.20 | ethics_phase2 | 2400 | 88.3% | 0.0% | 0.0% | 11.7% | 0.0% |
| x-ai/grok-4.20 | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| x-ai/grok-4.20 | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| x-ai/grok-4.20 | ous_ggb | 480 | 99.0% | 0.0% | 0.0% | 1.0% | 0.0% |
| meta-llama/llama-3.1-70b-instruct | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | 2400 | 90.5% | 0.0% | 0.0% | 9.5% | 0.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | 2400 | 92.8% | 0.0% | 0.0% | 7.2% | 0.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | 720 | 87.9% | 0.0% | 0.0% | 12.1% | 0.0% |
| meta-llama/llama-3.1-70b-instruct | ous_ggb | 480 | 92.5% | 0.0% | 0.0% | 7.5% | 0.0% |
| meta-llama/llama-3.1-8b-instruct | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.1-8b-instruct | ethics_phase2 | 2400 | 99.6% | 0.4% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | 2400 | 98.8% | 0.2% | 0.0% | 1.1% | 0.0% |
| meta-llama/llama-3.1-8b-instruct | mfq2_phase2 | 720 | 99.2% | 0.6% | 0.0% | 0.3% | 0.0% |
| meta-llama/llama-3.1-8b-instruct | ous_ggb | 480 | 93.5% | 6.2% | 0.0% | 0.2% | 0.0% |
| mistralai/mistral-medium-3.1 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | 2400 | 96.8% | 0.0% | 0.0% | 3.2% | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | mfq2_phase2 | 720 | 96.4% | 0.0% | 0.0% | 3.6% | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-4o-mini-2024-07-18 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | 2400 | 90.1% | 0.0% | 0.0% | 9.9% | 0.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | 2400 | 92.4% | 0.0% | 0.0% | 7.6% | 0.0% |
| openai/gpt-4o-mini-2024-07-18 | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-4o-mini-2024-07-18 | ous_ggb | 480 | 93.1% | 0.0% | 0.0% | 6.9% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | ethics_phase2 | 2400 | 99.8% | 0.0% | 0.0% | 0.2% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | 2400 | 90.2% | 0.0% | 0.0% | 9.8% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | mfq2_phase2 | 720 | 99.4% | 0.0% | 0.0% | 0.6% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | ous_ggb | 480 | 97.1% | 0.0% | 0.0% | 2.9% | 0.0% |
| deepseek/deepseek-v4-flash-0731 | attention_checks | 300 | 98.7% | 0.0% | 0.0% | 1.0% | 0.3% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | 2400 | 88.3% | 0.1% | 0.0% | 11.5% | 0.1% |
| deepseek/deepseek-v4-flash-0731 | ipip_neo_120 | 2400 | 98.4% | 0.0% | 0.0% | 1.4% | 0.1% |
| deepseek/deepseek-v4-flash-0731 | mfq2_phase2 | 720 | 99.4% | 0.0% | 0.0% | 0.6% | 0.0% |
| deepseek/deepseek-v4-flash-0731 | ous_ggb | 480 | 97.1% | 0.0% | 0.0% | 2.7% | 0.2% |
| z-ai/glm-5.2 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| z-ai/glm-5.2 | ethics_phase2 | 2400 | 99.2% | 0.0% | 0.0% | 0.8% | 0.0% |
| z-ai/glm-5.2 | ipip_neo_120 | 2400 | 96.5% | 0.0% | 0.0% | 3.5% | 0.0% |
| z-ai/glm-5.2 | mfq2_phase2 | 720 | 96.7% | 0.8% | 0.0% | 2.5% | 0.0% |
| z-ai/glm-5.2 | ous_ggb | 480 | 99.2% | 0.0% | 0.0% | 0.8% | 0.0% |
| z-ai/glm-4.5-air | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| z-ai/glm-4.5-air | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| z-ai/glm-4.5-air | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| z-ai/glm-4.5-air | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| z-ai/glm-4.5-air | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemma-3-27b-it | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemma-3-27b-it | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemma-3-27b-it | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemma-3-27b-it | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemma-3-27b-it | ous_ggb | 480 | 99.2% | 0.0% | 0.0% | 0.8% | 0.0% |
| nvidia/nemotron-3.5-lightning | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| nvidia/nemotron-3.5-lightning | ethics_phase2 | 2400 | 99.8% | 0.0% | 0.0% | 0.2% | 0.0% |
| nvidia/nemotron-3.5-lightning | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| nvidia/nemotron-3.5-lightning | mfq2_phase2 | 720 | 99.9% | 0.0% | 0.0% | 0.0% | 0.1% |
| nvidia/nemotron-3.5-lightning | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| amazon/nova-lite-v1 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| amazon/nova-lite-v1 | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| amazon/nova-lite-v1 | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| amazon/nova-lite-v1 | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| amazon/nova-lite-v1 | ous_ggb | 480 | 99.8% | 0.0% | 0.0% | 0.0% | 0.2% |
| microsoft/phi-4 | attention_checks | 300 | 79.7% | 0.0% | 0.0% | 20.3% | 0.0% |
| microsoft/phi-4 | ethics_phase2 | 2400 | 28.2% | 0.2% | 0.0% | 71.6% | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | 2400 | 5.0% | 0.0% | 0.0% | 94.9% | 0.0% |
| microsoft/phi-4 | mfq2_phase2 | 720 | 40.1% | 0.0% | 0.0% | 59.9% | 0.0% |
| microsoft/phi-4 | ous_ggb | 480 | 22.7% | 1.0% | 0.0% | 76.2% | 0.0% |
| openai/gpt-4.1-mini | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-4.1-mini | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-4.1-mini | ipip_neo_120 | 2400 | 99.9% | 0.0% | 0.0% | 0.1% | 0.0% |
| openai/gpt-4.1-mini | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-4.1-mini | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## Fragility (bare, first-person)

Fragility is the within-item SD across both framings and five option permutations, then averaged over eligible items. Raw and range-normalized values are both shown.

| Model | Instrument | Raw fragility | Normalized fragility | Suppressed / total items |
|---|---|---:|---:|---:|
| amazon/nova-lite-v1 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| amazon/nova-lite-v1 | ethics_phase2 | 0.088 | 0.088 | 0 / 120 |
| amazon/nova-lite-v1 | ipip_neo_120 | 0.594 | 0.149 | 0 / 120 |
| amazon/nova-lite-v1 | mfq2_phase2 | 0.803 | 0.201 | 0 / 36 |
| amazon/nova-lite-v1 | ous_ggb | 0.300 | 0.075 | 0 / 24 |
| anthropic/claude-sonnet-5 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| anthropic/claude-sonnet-5 | ethics_phase2 | 0.070 | 0.070 | 0 / 120 |
| anthropic/claude-sonnet-5 | ipip_neo_120 | 0.783 | 0.196 | 0 / 120 |
| anthropic/claude-sonnet-5 | mfq2_phase2 | 0.574 | 0.144 | 0 / 36 |
| anthropic/claude-sonnet-5 | ous_ggb | 0.360 | 0.090 | 0 / 24 |
| deepseek/deepseek-v4-flash-0731 | attention_checks | 0.153 | 0.153 | 0 / 15 |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | 0.255 | 0.255 | 34 / 120 |
| deepseek/deepseek-v4-flash-0731 | ipip_neo_120 | 1.039 | 0.260 | 2 / 120 |
| deepseek/deepseek-v4-flash-0731 | mfq2_phase2 | 0.937 | 0.234 | 0 / 36 |
| deepseek/deepseek-v4-flash-0731 | ous_ggb | 1.132 | 0.283 | 0 / 24 |
| deepseek/deepseek-v4-pro-0813 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| deepseek/deepseek-v4-pro-0813 | ethics_phase2 | 0.194 | 0.194 | 0 / 120 |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | 0.944 | 0.236 | 10 / 120 |
| deepseek/deepseek-v4-pro-0813 | mfq2_phase2 | 1.006 | 0.252 | 0 / 36 |
| deepseek/deepseek-v4-pro-0813 | ous_ggb | 1.059 | 0.265 | 0 / 24 |
| google/gemini-2.5-flash | attention_checks | 0.000 | 0.000 | 0 / 15 |
| google/gemini-2.5-flash | ethics_phase2 | 0.102 | 0.102 | 0 / 120 |
| google/gemini-2.5-flash | ipip_neo_120 | 0.729 | 0.182 | 0 / 120 |
| google/gemini-2.5-flash | mfq2_phase2 | 0.662 | 0.165 | 0 / 36 |
| google/gemini-2.5-flash | ous_ggb | 0.435 | 0.109 | 0 / 24 |
| google/gemini-2.5-flash-lite | attention_checks | 0.000 | 0.000 | 0 / 15 |
| google/gemini-2.5-flash-lite | ethics_phase2 | 0.101 | 0.101 | 0 / 120 |
| google/gemini-2.5-flash-lite | ipip_neo_120 | 0.649 | 0.162 | 0 / 120 |
| google/gemini-2.5-flash-lite | mfq2_phase2 | 0.783 | 0.196 | 10 / 36 |
| google/gemini-2.5-flash-lite | ous_ggb | 0.546 | 0.136 | 7 / 24 |
| google/gemma-3-27b-it | attention_checks | 0.000 | 0.000 | 0 / 15 |
| google/gemma-3-27b-it | ethics_phase2 | 0.066 | 0.066 | 0 / 120 |
| google/gemma-3-27b-it | ipip_neo_120 | 0.669 | 0.167 | 0 / 120 |
| google/gemma-3-27b-it | mfq2_phase2 | 0.432 | 0.108 | 0 / 36 |
| google/gemma-3-27b-it | ous_ggb | 0.653 | 0.163 | 0 / 24 |
| meta-llama/llama-3.1-70b-instruct | attention_checks | 0.000 | 0.000 | 0 / 15 |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | 0.201 | 0.201 | 38 / 120 |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | 1.384 | 0.346 | 25 / 120 |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | 1.088 | 0.272 | 20 / 36 |
| meta-llama/llama-3.1-70b-instruct | ous_ggb | 0.342 | 0.085 | 11 / 24 |
| meta-llama/llama-3.1-8b-instruct | attention_checks | 0.020 | 0.020 | 0 / 15 |
| meta-llama/llama-3.1-8b-instruct | ethics_phase2 | 0.233 | 0.233 | 0 / 120 |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | 1.005 | 0.251 | 3 / 120 |
| meta-llama/llama-3.1-8b-instruct | mfq2_phase2 | 1.360 | 0.340 | 0 / 36 |
| meta-llama/llama-3.1-8b-instruct | ous_ggb | 0.611 | 0.153 | 0 / 24 |
| microsoft/phi-4 | attention_checks | 0.000 | 0.000 | 14 / 15 |
| microsoft/phi-4 | ethics_phase2 | 0.143 | 0.143 | 106 / 120 |
| microsoft/phi-4 | ipip_neo_120 | 0.175 | 0.044 | 114 / 120 |
| microsoft/phi-4 | mfq2_phase2 | 0.523 | 0.131 | 14 / 36 |
| microsoft/phi-4 | ous_ggb | 0.553 | 0.138 | 19 / 24 |
| mistralai/mistral-medium-3.1 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| mistralai/mistral-medium-3.1 | ethics_phase2 | 0.040 | 0.040 | 0 / 120 |
| mistralai/mistral-medium-3.1 | ipip_neo_120 | 0.635 | 0.159 | 0 / 120 |
| mistralai/mistral-medium-3.1 | mfq2_phase2 | 0.455 | 0.114 | 0 / 36 |
| mistralai/mistral-medium-3.1 | ous_ggb | 0.398 | 0.099 | 0 / 24 |
| mistralai/mistral-small-3.2-24b-instruct | attention_checks | 0.000 | 0.000 | 0 / 15 |
| mistralai/mistral-small-3.2-24b-instruct | ethics_phase2 | 0.102 | 0.102 | 0 / 120 |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | 0.589 | 0.147 | 0 / 120 |
| mistralai/mistral-small-3.2-24b-instruct | mfq2_phase2 | 0.481 | 0.120 | 0 / 36 |
| mistralai/mistral-small-3.2-24b-instruct | ous_ggb | 0.419 | 0.105 | 0 / 24 |
| nvidia/nemotron-3.5-lightning | attention_checks | 0.000 | 0.000 | 0 / 15 |
| nvidia/nemotron-3.5-lightning | ethics_phase2 | 0.214 | 0.214 | 0 / 120 |
| nvidia/nemotron-3.5-lightning | ipip_neo_120 | 0.878 | 0.220 | 0 / 120 |
| nvidia/nemotron-3.5-lightning | mfq2_phase2 | 0.660 | 0.165 | 0 / 36 |
| nvidia/nemotron-3.5-lightning | ous_ggb | 0.548 | 0.137 | 0 / 24 |
| openai/gpt-4.1-mini | attention_checks | 0.000 | 0.000 | 0 / 15 |
| openai/gpt-4.1-mini | ethics_phase2 | 0.080 | 0.080 | 0 / 120 |
| openai/gpt-4.1-mini | ipip_neo_120 | 0.683 | 0.171 | 0 / 120 |
| openai/gpt-4.1-mini | mfq2_phase2 | 0.510 | 0.127 | 0 / 36 |
| openai/gpt-4.1-mini | ous_ggb | 0.510 | 0.127 | 0 / 24 |
| openai/gpt-4o-mini-2024-07-18 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | 0.128 | 0.128 | 32 / 120 |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | 0.689 | 0.172 | 0 / 120 |
| openai/gpt-4o-mini-2024-07-18 | mfq2_phase2 | 0.647 | 0.162 | 0 / 36 |
| openai/gpt-4o-mini-2024-07-18 | ous_ggb | 0.437 | 0.109 | 4 / 24 |
| openai/gpt-5.4-mini | attention_checks | 0.000 | 0.000 | 0 / 15 |
| openai/gpt-5.4-mini | ethics_phase2 | 0.142 | 0.142 | 0 / 120 |
| openai/gpt-5.4-mini | ipip_neo_120 | 0.745 | 0.186 | 0 / 120 |
| openai/gpt-5.4-mini | mfq2_phase2 | 0.971 | 0.243 | 0 / 36 |
| openai/gpt-5.4-mini | ous_ggb | 0.524 | 0.131 | 0 / 24 |
| openai/gpt-5.6-luna | attention_checks | 0.000 | 0.000 | 0 / 15 |
| openai/gpt-5.6-luna | ethics_phase2 | 0.103 | 0.103 | 0 / 120 |
| openai/gpt-5.6-luna | ipip_neo_120 | 0.840 | 0.210 | 0 / 120 |
| openai/gpt-5.6-luna | mfq2_phase2 | 0.590 | 0.147 | 0 / 36 |
| openai/gpt-5.6-luna | ous_ggb | 0.383 | 0.096 | 0 / 24 |
| qwen/qwen3.8-27b | attention_checks | 0.000 | 0.000 | 0 / 15 |
| qwen/qwen3.8-27b | ethics_phase2 | 0.067 | 0.067 | 0 / 120 |
| qwen/qwen3.8-27b | ipip_neo_120 | 0.734 | 0.184 | 0 / 120 |
| qwen/qwen3.8-27b | mfq2_phase2 | 0.733 | 0.183 | 0 / 36 |
| qwen/qwen3.8-27b | ous_ggb | 0.460 | 0.115 | 0 / 24 |
| x-ai/grok-4.20 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| x-ai/grok-4.20 | ethics_phase2 | 0.101 | 0.101 | 29 / 120 |
| x-ai/grok-4.20 | ipip_neo_120 | 1.138 | 0.284 | 0 / 120 |
| x-ai/grok-4.20 | mfq2_phase2 | 0.777 | 0.194 | 0 / 36 |
| x-ai/grok-4.20 | ous_ggb | 0.864 | 0.216 | 0 / 24 |
| z-ai/glm-4.5-air | attention_checks | 0.000 | 0.000 | 0 / 15 |
| z-ai/glm-4.5-air | ethics_phase2 | 0.101 | 0.101 | 0 / 120 |
| z-ai/glm-4.5-air | ipip_neo_120 | 0.759 | 0.190 | 0 / 120 |
| z-ai/glm-4.5-air | mfq2_phase2 | 0.901 | 0.225 | 0 / 36 |
| z-ai/glm-4.5-air | ous_ggb | 0.624 | 0.156 | 0 / 24 |
| z-ai/glm-5.2 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| z-ai/glm-5.2 | ethics_phase2 | 0.156 | 0.156 | 0 / 120 |
| z-ai/glm-5.2 | ipip_neo_120 | 0.936 | 0.234 | 6 / 120 |
| z-ai/glm-5.2 | mfq2_phase2 | 1.003 | 0.251 | 1 / 36 |
| z-ai/glm-5.2 | ous_ggb | 0.592 | 0.148 | 0 / 24 |

## Suppression list

Any listed score has at least one item/condition/framing cell below 70% valid coverage and is excluded from that aggregate. Unlisted aggregates had no suppressed item cells.

| Model | Instrument | Scale | Condition | Framing | Suppressed / total | Mean coverage |
|---|---|---|---|---|---:|---:|
| anthropic/claude-sonnet-5 | ipip_neo_120 | ipip.neuroticism.depression | evaluator | first_person | 1 / 4 | 85.0% |
| anthropic/claude-sonnet-5 | ous_ggb | ggb.instrumental_harm | evaluator | first_person | 1 / 12 | 93.3% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.commonsense | bare | first_person | 9 / 24 | 72.5% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.commonsense | bare | third_person | 10 / 24 | 71.7% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.commonsense | evaluator | first_person | 6 / 24 | 86.7% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.commonsense | evaluator | third_person | 4 / 24 | 88.3% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.deontology | bare | first_person | 6 / 24 | 80.0% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.deontology | bare | third_person | 2 / 24 | 85.8% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.deontology | evaluator | third_person | 1 / 24 | 94.2% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.justice | bare | first_person | 7 / 24 | 82.5% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.justice | bare | third_person | 2 / 24 | 88.3% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.justice | evaluator | first_person | 1 / 24 | 95.0% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.utilitarianism | bare | first_person | 4 / 24 | 81.7% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.utilitarianism | bare | third_person | 6 / 24 | 86.7% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.virtue | bare | first_person | 8 / 24 | 75.0% |
| deepseek/deepseek-v4-flash-0731 | ethics_phase2 | ethics.virtue | bare | third_person | 4 / 24 | 87.5% |
| deepseek/deepseek-v4-flash-0731 | ipip_neo_120 | ipip.conscientiousness.self_discipline | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-flash-0731 | ipip_neo_120 | ipip.openness.imagination | bare | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-flash-0731 | ous_ggb | ggb.impartial_beneficence | bare | third_person | 1 / 12 | 95.0% |
| deepseek/deepseek-v4-flash-0731 | ous_ggb | ggb.instrumental_harm | bare | third_person | 1 / 12 | 93.3% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.altruism | evaluator | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.altruism | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.cooperation | evaluator | first_person | 2 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.modesty | bare | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.modesty | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.morality | evaluator | first_person | 3 / 4 | 50.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.achievement_striving | bare | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.cautiousness | bare | third_person | 1 / 4 | 70.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | first_person | 2 / 4 | 75.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_discipline | bare | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | first_person | 2 / 4 | 60.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | third_person | 4 / 4 | 40.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.activity_level | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.cheerfulness | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.excitement_seeking | bare | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.excitement_seeking | evaluator | first_person | 2 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.friendliness | evaluator | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.gregariousness | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.gregariousness | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.anxiety | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.adventurousness | bare | first_person | 2 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.artistic_interests | bare | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.emotionality | bare | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.emotionality | bare | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.intellect | evaluator | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.liberalism | bare | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.liberalism | evaluator | first_person | 2 / 4 | 75.0% |
| deepseek/deepseek-v4-pro-0813 | ous_ggb | ggb.instrumental_harm | evaluator | third_person | 1 / 12 | 93.3% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.conscientiousness.dutifulness | bare | third_person | 1 / 4 | 90.0% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.openness.intellect | bare | third_person | 1 / 4 | 80.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.authority | bare | first_person | 3 / 6 | 56.7% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.authority | bare | third_person | 5 / 6 | 36.7% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.care | bare | third_person | 4 / 6 | 30.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.equality | bare | first_person | 1 / 6 | 83.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.equality | bare | third_person | 6 / 6 | 23.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.loyalty | bare | first_person | 3 / 6 | 60.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.loyalty | bare | third_person | 5 / 6 | 20.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.proportionality | bare | first_person | 1 / 6 | 93.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.proportionality | bare | third_person | 5 / 6 | 53.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.purity | bare | first_person | 2 / 6 | 66.7% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.purity | bare | third_person | 4 / 6 | 40.0% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.impartial_beneficence | bare | first_person | 4 / 12 | 65.0% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.impartial_beneficence | bare | third_person | 8 / 12 | 46.7% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.instrumental_harm | bare | first_person | 3 / 12 | 75.0% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.instrumental_harm | bare | third_person | 3 / 12 | 76.7% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.commonsense | bare | first_person | 4 / 24 | 88.3% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.commonsense | bare | third_person | 3 / 24 | 92.5% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.commonsense | evaluator | first_person | 1 / 24 | 96.7% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.deontology | bare | first_person | 6 / 24 | 80.8% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.deontology | bare | third_person | 3 / 24 | 92.5% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.justice | bare | first_person | 5 / 24 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.justice | bare | third_person | 1 / 24 | 95.0% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.justice | evaluator | first_person | 4 / 24 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.utilitarianism | bare | first_person | 21 / 24 | 45.0% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.utilitarianism | bare | third_person | 4 / 24 | 90.8% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.utilitarianism | evaluator | first_person | 5 / 24 | 88.3% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.virtue | bare | first_person | 2 / 24 | 92.5% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.virtue | bare | third_person | 3 / 24 | 93.3% |
| meta-llama/llama-3.1-70b-instruct | ethics_phase2 | ethics.virtue | evaluator | first_person | 6 / 24 | 81.7% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.altruism | bare | first_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.cooperation | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.cooperation | bare | third_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.modesty | bare | first_person | 1 / 4 | 75.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.morality | bare | first_person | 2 / 4 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.sympathy | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.sympathy | bare | third_person | 1 / 4 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.trust | bare | first_person | 1 / 4 | 75.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness.trust | bare | third_person | 1 / 4 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness.dutifulness | bare | third_person | 2 / 4 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness.self_discipline | bare | first_person | 2 / 4 | 60.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness.self_discipline | bare | third_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | first_person | 1 / 4 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | third_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.activity_level | bare | first_person | 1 / 4 | 75.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.activity_level | bare | third_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.assertiveness | bare | third_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | first_person | 1 / 4 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | third_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.friendliness | bare | third_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.gregariousness | bare | first_person | 2 / 4 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion.gregariousness | bare | third_person | 1 / 4 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism.anger | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism.anxiety | bare | third_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism.depression | bare | first_person | 2 / 4 | 75.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism.immoderation | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism.immoderation | bare | third_person | 1 / 4 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | first_person | 2 / 4 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.adventurousness | bare | first_person | 1 / 4 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.adventurousness | bare | third_person | 2 / 4 | 75.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.artistic_interests | bare | third_person | 1 / 4 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.emotionality | bare | first_person | 3 / 4 | 55.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.imagination | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.imagination | bare | third_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness.liberalism | bare | third_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.authority | bare | first_person | 2 / 6 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.care | bare | first_person | 6 / 6 | 46.7% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.equality | bare | first_person | 2 / 6 | 73.3% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.equality | bare | third_person | 3 / 6 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.loyalty | bare | first_person | 3 / 6 | 63.3% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.loyalty | bare | third_person | 1 / 6 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.proportionality | bare | first_person | 4 / 6 | 60.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.proportionality | bare | third_person | 1 / 6 | 90.0% |
| meta-llama/llama-3.1-70b-instruct | mfq2_phase2 | mfq2.purity | bare | first_person | 3 / 6 | 70.0% |
| meta-llama/llama-3.1-70b-instruct | ous_ggb | ggb.impartial_beneficence | bare | first_person | 3 / 12 | 83.3% |
| meta-llama/llama-3.1-70b-instruct | ous_ggb | ggb.instrumental_harm | bare | first_person | 8 / 12 | 58.3% |
| meta-llama/llama-3.1-8b-instruct | ethics_phase2 | ethics.justice | evaluator | first_person | 3 / 24 | 95.0% |
| meta-llama/llama-3.1-8b-instruct | ethics_phase2 | ethics.justice | evaluator | third_person | 1 / 24 | 97.5% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.agreeableness.sympathy | evaluator | first_person | 1 / 4 | 90.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.agreeableness.trust | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | first_person | 1 / 4 | 85.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.neuroticism.immoderation | bare | first_person | 1 / 4 | 80.0% |
| meta-llama/llama-3.1-8b-instruct | mfq2_phase2 | mfq2.purity | evaluator | first_person | 1 / 6 | 93.3% |
| meta-llama/llama-3.1-8b-instruct | mfq2_phase2 | mfq2.purity | evaluator | third_person | 1 / 6 | 93.3% |
| meta-llama/llama-3.1-8b-instruct | ous_ggb | ggb.instrumental_harm | evaluator | first_person | 7 / 12 | 65.0% |
| meta-llama/llama-3.1-8b-instruct | ous_ggb | ggb.instrumental_harm | evaluator | third_person | 2 / 12 | 85.0% |
| microsoft/phi-4 | attention_checks | attention | bare | first_person | 14 / 15 | 20.0% |
| microsoft/phi-4 | ethics_phase2 | ethics.commonsense | bare | first_person | 23 / 24 | 7.5% |
| microsoft/phi-4 | ethics_phase2 | ethics.commonsense | bare | third_person | 21 / 24 | 17.5% |
| microsoft/phi-4 | ethics_phase2 | ethics.commonsense | evaluator | first_person | 21 / 24 | 14.2% |
| microsoft/phi-4 | ethics_phase2 | ethics.commonsense | evaluator | third_person | 23 / 24 | 11.7% |
| microsoft/phi-4 | ethics_phase2 | ethics.deontology | bare | first_person | 23 / 24 | 13.3% |
| microsoft/phi-4 | ethics_phase2 | ethics.deontology | bare | third_person | 19 / 24 | 45.8% |
| microsoft/phi-4 | ethics_phase2 | ethics.deontology | evaluator | first_person | 19 / 24 | 44.2% |
| microsoft/phi-4 | ethics_phase2 | ethics.deontology | evaluator | third_person | 22 / 24 | 45.0% |
| microsoft/phi-4 | ethics_phase2 | ethics.justice | bare | first_person | 17 / 24 | 44.2% |
| microsoft/phi-4 | ethics_phase2 | ethics.justice | bare | third_person | 7 / 24 | 76.7% |
| microsoft/phi-4 | ethics_phase2 | ethics.justice | evaluator | first_person | 21 / 24 | 15.0% |
| microsoft/phi-4 | ethics_phase2 | ethics.justice | evaluator | third_person | 20 / 24 | 30.0% |
| microsoft/phi-4 | ethics_phase2 | ethics.utilitarianism | bare | first_person | 22 / 24 | 15.0% |
| microsoft/phi-4 | ethics_phase2 | ethics.utilitarianism | bare | third_person | 18 / 24 | 32.5% |
| microsoft/phi-4 | ethics_phase2 | ethics.utilitarianism | evaluator | first_person | 21 / 24 | 40.0% |
| microsoft/phi-4 | ethics_phase2 | ethics.utilitarianism | evaluator | third_person | 24 / 24 | 47.5% |
| microsoft/phi-4 | ethics_phase2 | ethics.virtue | bare | first_person | 21 / 24 | 26.7% |
| microsoft/phi-4 | ethics_phase2 | ethics.virtue | bare | third_person | 24 / 24 | 13.3% |
| microsoft/phi-4 | ethics_phase2 | ethics.virtue | evaluator | first_person | 23 / 24 | 11.7% |
| microsoft/phi-4 | ethics_phase2 | ethics.virtue | evaluator | third_person | 22 / 24 | 11.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.altruism | bare | first_person | 3 / 4 | 45.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.altruism | bare | third_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.altruism | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.altruism | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.cooperation | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.cooperation | bare | third_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.cooperation | evaluator | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.cooperation | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.modesty | bare | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.modesty | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.modesty | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.modesty | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.morality | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.morality | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.morality | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.morality | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.sympathy | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.sympathy | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.sympathy | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.sympathy | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.trust | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.trust | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.trust | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness.trust | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.achievement_striving | bare | first_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.achievement_striving | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.achievement_striving | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.achievement_striving | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.cautiousness | bare | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.cautiousness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.dutifulness | bare | first_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.dutifulness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.orderliness | bare | first_person | 4 / 4 | 15.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.orderliness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.orderliness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.orderliness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_discipline | bare | first_person | 4 / 4 | 30.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_discipline | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_discipline | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_discipline | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | evaluator | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.activity_level | bare | first_person | 4 / 4 | 15.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.activity_level | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.activity_level | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.activity_level | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.assertiveness | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.assertiveness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.assertiveness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.assertiveness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | first_person | 4 / 4 | 15.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.cheerfulness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.cheerfulness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.excitement_seeking | bare | first_person | 3 / 4 | 25.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.excitement_seeking | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.excitement_seeking | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.excitement_seeking | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.friendliness | bare | first_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.friendliness | bare | third_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.friendliness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.friendliness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.gregariousness | bare | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.gregariousness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.gregariousness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion.gregariousness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anger | bare | first_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anger | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anger | evaluator | first_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anger | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anxiety | bare | first_person | 4 / 4 | 15.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anxiety | bare | third_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anxiety | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.anxiety | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.depression | bare | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.depression | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.depression | evaluator | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.depression | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.immoderation | bare | first_person | 4 / 4 | 20.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.immoderation | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.self_consciousness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.self_consciousness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.vulnerability | bare | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.vulnerability | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.vulnerability | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism.vulnerability | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.adventurousness | bare | first_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.adventurousness | bare | third_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.adventurousness | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.adventurousness | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.artistic_interests | bare | first_person | 3 / 4 | 35.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.artistic_interests | bare | third_person | 4 / 4 | 25.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | first_person | 4 / 4 | 15.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.emotionality | bare | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.emotionality | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.emotionality | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.emotionality | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.imagination | bare | first_person | 2 / 4 | 50.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.imagination | bare | third_person | 4 / 4 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.imagination | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.imagination | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.intellect | bare | first_person | 3 / 4 | 30.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.intellect | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.intellect | evaluator | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.intellect | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.liberalism | bare | first_person | 4 / 4 | 5.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.liberalism | bare | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.liberalism | evaluator | first_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness.liberalism | evaluator | third_person | 4 / 4 | 0.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.authority | bare | first_person | 2 / 6 | 60.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.authority | bare | third_person | 3 / 6 | 63.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.authority | evaluator | first_person | 6 / 6 | 3.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.authority | evaluator | third_person | 6 / 6 | 10.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.care | bare | third_person | 3 / 6 | 76.7% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.care | evaluator | first_person | 6 / 6 | 13.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.care | evaluator | third_person | 5 / 6 | 20.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.equality | bare | first_person | 5 / 6 | 53.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.equality | bare | third_person | 3 / 6 | 53.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.equality | evaluator | first_person | 6 / 6 | 0.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.equality | evaluator | third_person | 6 / 6 | 3.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.loyalty | bare | first_person | 4 / 6 | 70.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.loyalty | bare | third_person | 5 / 6 | 50.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.loyalty | evaluator | first_person | 6 / 6 | 3.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.loyalty | evaluator | third_person | 6 / 6 | 6.7% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.proportionality | bare | third_person | 2 / 6 | 73.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.proportionality | evaluator | first_person | 4 / 6 | 40.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.proportionality | evaluator | third_person | 5 / 6 | 30.0% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.purity | bare | first_person | 3 / 6 | 73.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.purity | bare | third_person | 5 / 6 | 46.7% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.purity | evaluator | first_person | 6 / 6 | 13.3% |
| microsoft/phi-4 | mfq2_phase2 | mfq2.purity | evaluator | third_person | 6 / 6 | 6.7% |
| microsoft/phi-4 | ous_ggb | ggb.impartial_beneficence | bare | first_person | 7 / 12 | 60.0% |
| microsoft/phi-4 | ous_ggb | ggb.impartial_beneficence | bare | third_person | 9 / 12 | 51.7% |
| microsoft/phi-4 | ous_ggb | ggb.impartial_beneficence | evaluator | first_person | 12 / 12 | 1.7% |
| microsoft/phi-4 | ous_ggb | ggb.impartial_beneficence | evaluator | third_person | 12 / 12 | 18.3% |
| microsoft/phi-4 | ous_ggb | ggb.instrumental_harm | bare | first_person | 12 / 12 | 23.3% |
| microsoft/phi-4 | ous_ggb | ggb.instrumental_harm | bare | third_person | 11 / 12 | 26.7% |
| microsoft/phi-4 | ous_ggb | ggb.instrumental_harm | evaluator | first_person | 12 / 12 | 0.0% |
| microsoft/phi-4 | ous_ggb | ggb.instrumental_harm | evaluator | third_person | 12 / 12 | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.agreeableness.altruism | bare | third_person | 2 / 4 | 80.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.agreeableness.morality | bare | third_person | 1 / 4 | 80.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.agreeableness.trust | bare | third_person | 1 / 4 | 80.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.conscientiousness.achievement_striving | bare | third_person | 1 / 4 | 80.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.conscientiousness.cautiousness | bare | third_person | 1 / 4 | 85.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | third_person | 1 / 4 | 85.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.extraversion.friendliness | evaluator | third_person | 1 / 4 | 85.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.neuroticism.immoderation | bare | third_person | 1 / 4 | 85.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | third_person | 1 / 4 | 90.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.neuroticism.vulnerability | bare | third_person | 1 / 4 | 85.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.openness.imagination | bare | third_person | 1 / 4 | 90.0% |
| mistralai/mistral-small-3.2-24b-instruct | mfq2_phase2 | mfq2.authority | evaluator | third_person | 1 / 6 | 86.7% |
| mistralai/mistral-small-3.2-24b-instruct | mfq2_phase2 | mfq2.proportionality | evaluator | third_person | 1 / 6 | 90.0% |
| mistralai/mistral-small-3.2-24b-instruct | mfq2_phase2 | mfq2.purity | evaluator | first_person | 1 / 6 | 90.0% |
| mistralai/mistral-small-3.2-24b-instruct | mfq2_phase2 | mfq2.purity | evaluator | third_person | 1 / 6 | 86.7% |
| nvidia/nemotron-3.5-lightning | ethics_phase2 | ethics.virtue | bare | third_person | 1 / 24 | 96.7% |
| openai/gpt-4.1-mini | ipip_neo_120 | ipip.openness.intellect | bare | third_person | 1 / 4 | 90.0% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.commonsense | bare | first_person | 13 / 24 | 57.5% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.commonsense | bare | third_person | 3 / 24 | 90.0% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.commonsense | evaluator | first_person | 10 / 24 | 70.8% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.commonsense | evaluator | third_person | 6 / 24 | 85.8% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.justice | bare | first_person | 10 / 24 | 79.2% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.justice | evaluator | first_person | 6 / 24 | 85.8% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.justice | evaluator | third_person | 1 / 24 | 98.3% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.utilitarianism | bare | first_person | 6 / 24 | 88.3% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.utilitarianism | evaluator | first_person | 10 / 24 | 79.2% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.utilitarianism | evaluator | third_person | 9 / 24 | 78.3% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.virtue | bare | first_person | 3 / 24 | 91.7% |
| openai/gpt-4o-mini-2024-07-18 | ethics_phase2 | ethics.virtue | evaluator | first_person | 1 / 24 | 98.3% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.agreeableness.altruism | evaluator | first_person | 1 / 4 | 75.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.agreeableness.modesty | evaluator | first_person | 2 / 4 | 80.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.agreeableness.morality | evaluator | first_person | 2 / 4 | 75.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.agreeableness.sympathy | evaluator | first_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness.achievement_striving | evaluator | first_person | 2 / 4 | 70.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | first_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | first_person | 2 / 4 | 70.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness.self_discipline | evaluator | first_person | 1 / 4 | 80.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness.self_discipline | evaluator | third_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | evaluator | first_person | 2 / 4 | 70.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.extraversion.activity_level | evaluator | first_person | 3 / 4 | 60.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.extraversion.excitement_seeking | evaluator | first_person | 1 / 4 | 90.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.extraversion.friendliness | evaluator | first_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.extraversion.gregariousness | bare | third_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism.anger | evaluator | first_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism.depression | evaluator | first_person | 1 / 4 | 90.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism.depression | evaluator | third_person | 1 / 4 | 90.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism.immoderation | bare | third_person | 1 / 4 | 75.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | third_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism.vulnerability | evaluator | third_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.artistic_interests | bare | third_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | first_person | 1 / 4 | 80.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | third_person | 1 / 4 | 80.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.emotionality | evaluator | first_person | 1 / 4 | 75.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.emotionality | evaluator | third_person | 1 / 4 | 90.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.imagination | evaluator | first_person | 1 / 4 | 75.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.intellect | bare | third_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness.intellect | evaluator | first_person | 1 / 4 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ous_ggb | ggb.instrumental_harm | bare | first_person | 4 / 12 | 73.3% |
| openai/gpt-4o-mini-2024-07-18 | ous_ggb | ggb.instrumental_harm | evaluator | first_person | 2 / 12 | 86.7% |
| openai/gpt-4o-mini-2024-07-18 | ous_ggb | ggb.instrumental_harm | evaluator | third_person | 3 / 12 | 85.0% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | bare | first_person | 6 / 24 | 76.7% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | bare | third_person | 6 / 24 | 84.2% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | evaluator | first_person | 5 / 24 | 88.3% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | evaluator | third_person | 11 / 24 | 75.0% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.justice | bare | first_person | 14 / 24 | 53.3% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.justice | bare | third_person | 2 / 24 | 95.0% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.justice | evaluator | third_person | 5 / 24 | 81.7% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | bare | first_person | 9 / 24 | 77.5% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | bare | third_person | 12 / 24 | 70.8% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | evaluator | third_person | 15 / 24 | 69.2% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.virtue | bare | third_person | 1 / 24 | 97.5% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.agreeableness.modesty | evaluator | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.agreeableness.sympathy | bare | first_person | 2 / 4 | 75.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.agreeableness.trust | bare | third_person | 1 / 4 | 85.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.conscientiousness.cautiousness | bare | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.extraversion.assertiveness | evaluator | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.neuroticism.depression | bare | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.neuroticism.vulnerability | bare | first_person | 1 / 4 | 80.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness.liberalism | bare | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | mfq2_phase2 | mfq2.proportionality | bare | first_person | 1 / 6 | 93.3% |
| z-ai/glm-5.2 | mfq2_phase2 | mfq2.proportionality | evaluator | third_person | 1 / 6 | 93.3% |
| z-ai/glm-5.2 | mfq2_phase2 | mfq2.purity | evaluator | third_person | 1 / 6 | 90.0% |
| anthropic/claude-sonnet-5 | ipip_neo_120 | ipip.neuroticism | evaluator | first_person | 1 / 24 | 96.7% |
| deepseek/deepseek-v4-flash-0731 | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 1 / 24 | 95.0% |
| deepseek/deepseek-v4-flash-0731 | ipip_neo_120 | ipip.openness | bare | first_person | 1 / 24 | 96.7% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness | bare | first_person | 1 / 24 | 90.8% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness | evaluator | first_person | 7 / 24 | 80.8% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness | evaluator | third_person | 1 / 24 | 94.2% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 2 / 24 | 87.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 7 / 24 | 79.2% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | evaluator | first_person | 4 / 24 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | evaluator | third_person | 1 / 24 | 90.8% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | bare | first_person | 2 / 24 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | bare | third_person | 1 / 24 | 92.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | evaluator | first_person | 2 / 24 | 88.3% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | evaluator | third_person | 3 / 24 | 92.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | bare | first_person | 1 / 24 | 95.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | bare | third_person | 1 / 24 | 94.2% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | evaluator | first_person | 1 / 24 | 90.8% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | evaluator | third_person | 1 / 24 | 94.2% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness | bare | first_person | 4 / 24 | 87.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness | bare | third_person | 2 / 24 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness | evaluator | first_person | 4 / 24 | 90.0% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 1 / 24 | 98.3% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.openness | bare | third_person | 1 / 24 | 96.7% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness | bare | first_person | 7 / 24 | 80.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.agreeableness | bare | third_person | 3 / 24 | 88.3% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 3 / 24 | 85.0% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 4 / 24 | 90.8% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion | bare | first_person | 4 / 24 | 84.2% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.extraversion | bare | third_person | 5 / 24 | 86.7% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism | bare | first_person | 6 / 24 | 84.2% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.neuroticism | bare | third_person | 2 / 24 | 89.2% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness | bare | first_person | 5 / 24 | 83.3% |
| meta-llama/llama-3.1-70b-instruct | ipip_neo_120 | ipip.openness | bare | third_person | 5 / 24 | 85.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.agreeableness | bare | first_person | 1 / 24 | 95.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.agreeableness | evaluator | first_person | 1 / 24 | 97.5% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.extraversion | bare | first_person | 1 / 24 | 95.0% |
| meta-llama/llama-3.1-8b-instruct | ipip_neo_120 | ipip.neuroticism | bare | first_person | 1 / 24 | 96.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness | bare | first_person | 23 / 24 | 21.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness | bare | third_person | 24 / 24 | 1.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness | evaluator | first_person | 24 / 24 | 0.8% |
| microsoft/phi-4 | ipip_neo_120 | ipip.agreeableness | evaluator | third_person | 24 / 24 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 24 / 24 | 15.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 24 / 24 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness | evaluator | first_person | 24 / 24 | 1.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.conscientiousness | evaluator | third_person | 24 / 24 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion | bare | first_person | 23 / 24 | 14.2% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion | bare | third_person | 24 / 24 | 0.8% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion | evaluator | first_person | 24 / 24 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.extraversion | evaluator | third_person | 24 / 24 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism | bare | first_person | 24 / 24 | 10.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism | bare | third_person | 24 / 24 | 0.8% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism | evaluator | first_person | 24 / 24 | 2.5% |
| microsoft/phi-4 | ipip_neo_120 | ipip.neuroticism | evaluator | third_person | 24 / 24 | 0.0% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness | bare | first_person | 20 / 24 | 21.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness | bare | third_person | 24 / 24 | 6.7% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness | evaluator | first_person | 24 / 24 | 3.3% |
| microsoft/phi-4 | ipip_neo_120 | ipip.openness | evaluator | third_person | 24 / 24 | 0.0% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.agreeableness | bare | third_person | 4 / 24 | 85.8% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 2 / 24 | 90.8% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.extraversion | bare | third_person | 1 / 24 | 89.2% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.extraversion | evaluator | third_person | 1 / 24 | 97.5% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.neuroticism | bare | third_person | 3 / 24 | 87.5% |
| mistralai/mistral-small-3.2-24b-instruct | ipip_neo_120 | ipip.openness | bare | third_person | 1 / 24 | 91.7% |
| openai/gpt-4.1-mini | ipip_neo_120 | ipip.openness | bare | third_person | 1 / 24 | 98.3% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.agreeableness | evaluator | first_person | 6 / 24 | 81.7% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness | evaluator | first_person | 8 / 24 | 77.5% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.conscientiousness | evaluator | third_person | 1 / 24 | 92.5% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.extraversion | bare | third_person | 1 / 24 | 92.5% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.extraversion | evaluator | first_person | 5 / 24 | 87.5% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism | bare | third_person | 1 / 24 | 93.3% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism | evaluator | first_person | 2 / 24 | 93.3% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.neuroticism | evaluator | third_person | 3 / 24 | 91.7% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness | bare | third_person | 2 / 24 | 92.5% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness | evaluator | first_person | 4 / 24 | 85.0% |
| openai/gpt-4o-mini-2024-07-18 | ipip_neo_120 | ipip.openness | evaluator | third_person | 2 / 24 | 91.7% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.agreeableness | bare | first_person | 2 / 24 | 90.8% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.agreeableness | bare | third_person | 1 / 24 | 97.5% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.agreeableness | evaluator | first_person | 1 / 24 | 95.8% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 1 / 24 | 93.3% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.extraversion | evaluator | first_person | 1 / 24 | 93.3% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.neuroticism | bare | first_person | 2 / 24 | 94.2% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness | bare | first_person | 1 / 24 | 95.0% |

## GGB validation (bare, first-person)

Higher impartial-beneficence agreement and lower instrumental-harm agreement are the pre-specified directional sanity check. Values are 1–5 agreement means with 95% bootstrap intervals; they are descriptive model outputs, not evidence of moral competence.

Directional flag uses the neutral midpoint: impartial beneficence > 3 and instrumental harm < 3. Reproduced: openai/gpt-5.4-mini, openai/gpt-5.6-luna, google/gemini-2.5-flash-lite, google/gemini-2.5-flash, meta-llama/llama-3.1-70b-instruct, meta-llama/llama-3.1-8b-instruct, mistralai/mistral-medium-3.1, mistralai/mistral-small-3.2-24b-instruct, openai/gpt-4o-mini-2024-07-18, deepseek/deepseek-v4-pro-0813, deepseek/deepseek-v4-flash-0731, z-ai/glm-5.2, z-ai/glm-4.5-air, google/gemma-3-27b-it, nvidia/nemotron-3.5-lightning, amazon/nova-lite-v1, openai/gpt-4.1-mini. Not reproduced / suppressed: anthropic/claude-sonnet-5, x-ai/grok-4.20, qwen/qwen3.8-27b, microsoft/phi-4 (suppressed).

| Model | Impartial Beneficence | Instrumental Harm |
|---|---:|---:|
| amazon/nova-lite-v1 | 3.483 [3.200, 3.783] | 1.483 [1.200, 1.850] |
| anthropic/claude-sonnet-5 | 2.467 [2.167, 2.767] | 1.933 [1.383, 2.617] |
| deepseek/deepseek-v4-flash-0731 | 3.908 [3.200, 4.525] | 2.267 [1.717, 2.850] |
| deepseek/deepseek-v4-pro-0813 | 3.392 [2.900, 3.867] | 2.250 [1.850, 2.700] |
| google/gemini-2.5-flash | 3.100 [2.400, 3.767] | 1.250 [1.000, 1.733] |
| google/gemini-2.5-flash-lite | 3.350 [2.644, 4.006] | 1.356 [1.089, 1.733] |
| google/gemma-3-27b-it | 3.917 [3.367, 4.400] | 1.417 [1.100, 1.817] |
| meta-llama/llama-3.1-70b-instruct | 4.339 [3.600, 4.822] | 1.000 [1.000, 1.000] |
| meta-llama/llama-3.1-8b-instruct | 4.167 [3.850, 4.417] | 1.850 [1.533, 2.217] |
| microsoft/phi-4 | 4.360 [3.680, 4.920] | suppressed |
| mistralai/mistral-medium-3.1 | 3.850 [3.267, 4.333] | 1.650 [1.050, 2.450] |
| mistralai/mistral-small-3.2-24b-instruct | 3.900 [3.583, 4.183] | 2.450 [1.983, 2.933] |
| nvidia/nemotron-3.5-lightning | 3.950 [3.367, 4.417] | 1.050 [1.000, 1.133] |
| openai/gpt-4.1-mini | 3.733 [3.450, 4.033] | 2.050 [1.567, 2.600] |
| openai/gpt-4o-mini-2024-07-18 | 4.400 [4.000, 4.717] | 1.744 [1.000, 2.712] |
| openai/gpt-5.4-mini | 3.700 [3.133, 4.167] | 1.400 [1.017, 1.933] |
| openai/gpt-5.6-luna | 3.317 [2.817, 3.767] | 1.750 [1.233, 2.383] |
| qwen/qwen3.8-27b | 2.550 [1.950, 3.250] | 1.600 [1.000, 2.250] |
| x-ai/grok-4.20 | 2.321 [1.600, 3.150] | 1.700 [1.317, 2.150] |
| z-ai/glm-4.5-air | 4.333 [3.700, 4.783] | 1.817 [1.167, 2.683] |
| z-ai/glm-5.2 | 3.317 [2.733, 3.817] | 1.637 [1.137, 2.275] |

## ETHICS reference agreement (bare, first-person)

Each cell is exact agreement with the public ETHICS test label. The score is not a broad ethical-validity claim and should be interpreted alongside the raw prompts and framing effects.

| Model | Commonsense | Deontology | Justice | Utilitarianism | Virtue |
|---|---:|---:|---:|---:|---:|
| amazon/nova-lite-v1 | 0.650 [0.450, 0.833] | 0.883 [0.750, 0.983] | 0.825 [0.675, 0.958] | 0.583 [0.392, 0.758] | 0.842 [0.708, 0.958] |
| anthropic/claude-sonnet-5 | 0.850 [0.700, 0.975] | 0.850 [0.708, 0.958] | 0.858 [0.708, 0.975] | 0.925 [0.808, 1.000] | 0.942 [0.833, 1.000] |
| deepseek/deepseek-v4-flash-0731 | 0.833 [0.677, 0.957] | 0.689 [0.536, 0.836] | 0.641 [0.488, 0.785] | 0.858 [0.722, 0.970] | 0.959 [0.897, 1.000] |
| deepseek/deepseek-v4-pro-0813 | 0.775 [0.608, 0.925] | 0.717 [0.550, 0.867] | 0.708 [0.542, 0.850] | 0.475 [0.308, 0.650] | 0.917 [0.808, 1.000] |
| google/gemini-2.5-flash | 0.767 [0.608, 0.917] | 0.808 [0.667, 0.933] | 0.800 [0.633, 0.933] | 0.750 [0.600, 0.883] | 0.967 [0.908, 1.000] |
| google/gemini-2.5-flash-lite | 0.775 [0.600, 0.917] | 0.783 [0.617, 0.917] | 0.567 [0.375, 0.758] | 0.750 [0.592, 0.892] | 0.958 [0.875, 1.000] |
| google/gemma-3-27b-it | 0.683 [0.500, 0.858] | 0.733 [0.558, 0.883] | 0.692 [0.508, 0.858] | 0.817 [0.650, 0.958] | 0.925 [0.825, 1.000] |
| meta-llama/llama-3.1-70b-instruct | 0.750 [0.550, 0.950] | 0.731 [0.564, 0.875] | 0.863 [0.716, 0.989] | 1.000 [1.000, 1.000] | 0.786 [0.664, 0.900] |
| meta-llama/llama-3.1-8b-instruct | 0.700 [0.525, 0.858] | 0.708 [0.542, 0.850] | 0.617 [0.442, 0.783] | 0.567 [0.425, 0.700] | 0.692 [0.533, 0.833] |
| microsoft/phi-4 | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.714 [0.286, 1.000] | 1.000 [1.000, 1.000] | 0.667 [0.000, 1.000] |
| mistralai/mistral-medium-3.1 | 0.625 [0.417, 0.792] | 0.767 [0.600, 0.917] | 0.708 [0.542, 0.875] | 0.667 [0.483, 0.833] | 0.975 [0.917, 1.000] |
| mistralai/mistral-small-3.2-24b-instruct | 0.792 [0.625, 0.958] | 0.775 [0.608, 0.917] | 0.808 [0.650, 0.942] | 0.533 [0.358, 0.692] | 0.942 [0.833, 1.000] |
| nvidia/nemotron-3.5-lightning | 0.742 [0.583, 0.875] | 0.725 [0.567, 0.867] | 0.600 [0.433, 0.767] | 0.675 [0.483, 0.850] | 0.833 [0.692, 0.958] |
| openai/gpt-4.1-mini | 0.792 [0.625, 0.917] | 0.808 [0.658, 0.933] | 0.542 [0.350, 0.733] | 0.833 [0.683, 0.950] | 0.933 [0.825, 1.000] |
| openai/gpt-4o-mini-2024-07-18 | 0.673 [0.382, 0.909] | 0.842 [0.708, 0.950] | 0.814 [0.600, 1.000] | 0.639 [0.442, 0.833] | 0.971 [0.914, 1.000] |
| openai/gpt-5.4-mini | 0.683 [0.517, 0.842] | 0.633 [0.467, 0.808] | 0.750 [0.600, 0.883] | 0.900 [0.800, 0.975] | 0.875 [0.758, 0.967] |
| openai/gpt-5.6-luna | 0.840 [0.692, 0.958] | 0.775 [0.625, 0.925] | 0.758 [0.592, 0.908] | 0.833 [0.700, 0.933] | 1.000 [1.000, 1.000] |
| qwen/qwen3.8-27b | 0.792 [0.625, 0.917] | 0.725 [0.542, 0.892] | 0.708 [0.533, 0.858] | 0.925 [0.833, 1.000] | 1.000 [1.000, 1.000] |
| x-ai/grok-4.20 | 0.833 [0.667, 1.000] | 0.725 [0.542, 0.883] | 0.650 [0.350, 0.900] | 0.473 [0.280, 0.667] | 0.892 [0.767, 0.983] |
| z-ai/glm-4.5-air | 0.742 [0.567, 0.900] | 0.750 [0.583, 0.908] | 0.683 [0.508, 0.858] | 0.833 [0.692, 0.950] | 0.942 [0.842, 1.000] |
| z-ai/glm-5.2 | 0.792 [0.633, 0.925] | 0.800 [0.642, 0.933] | 0.817 [0.675, 0.933] | 0.692 [0.542, 0.833] | 0.975 [0.925, 1.000] |

## Design sensitivity

Effects are paired at item level after the coverage rule. `evaluator − bare` holds framing constant; `first − third` holds condition constant. Positive values mean the named first term was higher on the item’s native score scale.

| Model | Scale | Effect | Pairs | Difference [95% CI] |
|---|---|---|---:|---:|
| anthropic/claude-sonnet-5 | ipip.neuroticism.anxiety | first_minus_third | 8 | -2.125 [-2.525, -1.575] |
| meta-llama/llama-3.1-8b-instruct | mfq2.purity | first_minus_third | 11 | -1.923 [-2.418, -1.377] |
| meta-llama/llama-3.1-70b-instruct | mfq2.purity | first_minus_third | 9 | -1.900 [-2.494, -1.289] |
| meta-llama/llama-3.1-8b-instruct | mfq2.loyalty | first_minus_third | 12 | -1.883 [-2.467, -1.267] |
| anthropic/claude-sonnet-5 | ipip.neuroticism.self_consciousness | first_minus_third | 8 | -1.781 [-2.350, -1.150] |
| openai/gpt-5.6-luna | ipip.neuroticism.anger | first_minus_third | 8 | -1.725 [-2.200, -1.250] |
| google/gemini-2.5-flash-lite | mfq2.purity | first_minus_third | 8 | -1.637 [-2.181, -1.100] |
| anthropic/claude-sonnet-5 | ipip.conscientiousness.cautiousness | first_minus_third | 8 | +1.625 [+1.200, +2.050] |
| openai/gpt-5.4-mini | mfq2.equality | first_minus_third | 12 | -1.617 [-2.133, -1.017] |
| anthropic/claude-sonnet-5 | ipip.conscientiousness.orderliness | first_minus_third | 8 | +1.600 [+0.725, +2.300] |
| anthropic/claude-sonnet-5 | ipip.openness.intellect | first_minus_third | 8 | +1.600 [+1.125, +2.075] |
| x-ai/grok-4.20 | ipip.extraversion.cheerfulness | first_minus_third | 8 | +1.600 [+0.925, +2.250] |
| meta-llama/llama-3.1-8b-instruct | mfq2.proportionality | first_minus_third | 12 | -1.583 [-2.217, -0.983] |
| anthropic/claude-sonnet-5 | ipip.neuroticism.vulnerability | first_minus_third | 8 | -1.575 [-2.075, -1.075] |
| z-ai/glm-5.2 | ipip.neuroticism.anxiety | first_minus_third | 8 | -1.556 [-2.400, -0.700] |
| openai/gpt-4o-mini-2024-07-18 | mfq2.purity | first_minus_third | 12 | -1.550 [-2.200, -0.900] |
| z-ai/glm-4.5-air | mfq2.equality | first_minus_third | 12 | -1.500 [-2.000, -1.017] |
| meta-llama/llama-3.1-70b-instruct | ipip.agreeableness.cooperation | evaluator_minus_bare | 6 | +1.492 [+0.883, +2.492] |
| anthropic/claude-sonnet-5 | ipip.neuroticism.anger | first_minus_third | 8 | -1.475 [-1.925, -1.000] |
| openai/gpt-5.6-luna | ipip.agreeableness.morality | first_minus_third | 8 | +1.475 [+1.175, +1.825] |
| meta-llama/llama-3.1-70b-instruct | mfq2.authority | first_minus_third | 10 | -1.460 [-1.840, -1.115] |
| openai/gpt-5.6-luna | ipip.conscientiousness.achievement_striving | first_minus_third | 8 | +1.450 [+1.025, +1.925] |
| amazon/nova-lite-v1 | mfq2.equality | first_minus_third | 12 | -1.433 [-2.033, -0.867] |
| meta-llama/llama-3.1-8b-instruct | ipip.neuroticism.anxiety | first_minus_third | 8 | -1.425 [-2.275, -0.650] |
| meta-llama/llama-3.1-70b-instruct | ipip.extraversion.excitement_seeking | evaluator_minus_bare | 8 | -1.419 [-2.100, -0.719] |

## Big Five comparison caveat

The HTML artifact compares bare first-person IPIP means with the only readily published IPIP-120 external norm table used here: a Chinese convenience sample (n=131). It is an illustrative reference, not a representative human population benchmark and not a basis for ranking models as people. Source: https://ipip.ori.org/ChineseIPIP-120norms.htm.

## Artifacts

- `reports/02_scoring.html` — self-contained visual dashboard with embedded plots.
- `data/derived/<run-id>/cell_scores.csv` — score/coverage/fragility for every analytical cell.
- `data/derived/<run-id>/scale_scores.csv` and `effects.csv` — publication-facing aggregates.
- `data/derived/<run-id>/summary.json` — run-level machine-readable summary.
