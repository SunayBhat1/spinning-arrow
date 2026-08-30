# Phase 2 main-battery report

**Run:** `20260830T155412Z__phase2__8fbf10`  
**Window:** 2026-08-30T15:54:12Z to 2026-08-30T16:57:17Z  
**Commit:** `5448d849db31656a4212a3151139d285aa6e4dcf`  
**Raw data:** `data/raw/20260830T155412Z__phase2__8fbf10/`  
**Manifest:** `data/manifests/20260830T155412Z__phase2__8fbf10.json`  
**Derived data:** `data/derived/20260830T155412Z__phase2__8fbf10/`  

## Decision-ready result

Phase 2 is complete and mechanically reproducible. Gate 2 remains pending user review; this report does not advance the project to Phase 3. Each score averages valid option permutations within an item/condition/framing cell. Cells below 70% valid coverage are suppressed; scale intervals use 2,000 deterministic item-and-permutation bootstraps.

## Run integrity and response quality

**Records:** 56,700 (6,300 per model)  
**OpenRouter-recorded cost:** $5.378043  
**Reasoning tokens in main battery:** 0 (hard requirement)

| Model | Parse | Attention | Refusal | Hedge | Unparseable | Error | Mean fragility | Suppressed cells | Cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| openai/gpt-5.4-mini | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.158 | 0 | $0.6078 |
| google/gemini-2.5-flash-lite | 95.9% | 100.0% | 0.0% | 0.0% | 4.1% | 0.0% | 0.120 | 62 | $0.0591 |
| anthropic/claude-sonnet-5 | 99.8% | 100.0% | 0.0% | 0.0% | 0.2% | 0.0% | 0.115 | 0 | $1.9784 |
| x-ai/grok-4.20 | 95.4% | 99.7% | 0.0% | 0.0% | 4.6% | 0.0% | 0.191 | 85 | $0.8481 |
| meta-llama/llama-3.3-70b-instruct | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.130 | 0 | $0.1295 |
| mistralai/mistral-medium-3.1 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.104 | 0 | $0.2275 |
| qwen/qwen3.8-27b | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.125 | 0 | $0.2916 |
| deepseek/deepseek-v4-pro-0813 | 95.8% | 99.7% | 0.0% | 0.0% | 4.2% | 0.0% | 0.198 | 58 | $0.7979 |
| z-ai/glm-5.2 | 98.6% | 100.0% | 0.1% | 0.0% | 1.2% | 0.0% | 0.158 | 14 | $0.4381 |

### Outcome classes by instrument

| Model | Instrument | Calls | Parse | Refusal | Hedge | Unparseable | Error |
|---|---|---:|---:|---:|---:|---:|---:|
| openai/gpt-5.4-mini | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| openai/gpt-5.4-mini | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash-lite | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash-lite | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | 2400 | 99.5% | 0.0% | 0.0% | 0.5% | 0.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | 720 | 77.6% | 0.0% | 0.0% | 22.4% | 0.0% |
| google/gemini-2.5-flash-lite | ous_ggb | 480 | 82.5% | 0.0% | 0.0% | 17.5% | 0.0% |
| anthropic/claude-sonnet-5 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| anthropic/claude-sonnet-5 | ipip_neo_120 | 2400 | 99.8% | 0.0% | 0.0% | 0.2% | 0.0% |
| anthropic/claude-sonnet-5 | mfq2_phase2 | 720 | 99.9% | 0.0% | 0.0% | 0.1% | 0.0% |
| anthropic/claude-sonnet-5 | ous_ggb | 480 | 99.4% | 0.0% | 0.0% | 0.6% | 0.0% |
| x-ai/grok-4.20 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| x-ai/grok-4.20 | ethics_phase2 | 2400 | 88.1% | 0.0% | 0.0% | 11.9% | 0.0% |
| x-ai/grok-4.20 | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| x-ai/grok-4.20 | mfq2_phase2 | 720 | 99.9% | 0.0% | 0.0% | 0.1% | 0.0% |
| x-ai/grok-4.20 | ous_ggb | 480 | 99.6% | 0.0% | 0.0% | 0.4% | 0.0% |
| meta-llama/llama-3.3-70b-instruct | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.3-70b-instruct | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.3-70b-instruct | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.3-70b-instruct | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| meta-llama/llama-3.3-70b-instruct | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| mistralai/mistral-medium-3.1 | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | ipip_neo_120 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | mfq2_phase2 | 720 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| qwen/qwen3.8-27b | ous_ggb | 480 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | attention_checks | 300 | 99.7% | 0.0% | 0.0% | 0.3% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | ethics_phase2 | 2400 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | 2400 | 89.8% | 0.0% | 0.0% | 10.2% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | mfq2_phase2 | 720 | 99.6% | 0.0% | 0.0% | 0.4% | 0.0% |
| deepseek/deepseek-v4-pro-0813 | ous_ggb | 480 | 97.7% | 0.0% | 0.0% | 2.3% | 0.0% |
| z-ai/glm-5.2 | attention_checks | 300 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| z-ai/glm-5.2 | ethics_phase2 | 2400 | 99.5% | 0.0% | 0.0% | 0.5% | 0.0% |
| z-ai/glm-5.2 | ipip_neo_120 | 2400 | 97.9% | 0.0% | 0.0% | 2.0% | 0.0% |
| z-ai/glm-5.2 | mfq2_phase2 | 720 | 97.6% | 1.0% | 0.0% | 1.4% | 0.0% |
| z-ai/glm-5.2 | ous_ggb | 480 | 98.3% | 0.2% | 0.0% | 1.5% | 0.0% |

## Fragility (bare, first-person)

Fragility is the within-item SD across both framings and five option permutations, then averaged over eligible items. Raw and range-normalized values are both shown.

| Model | Instrument | Raw fragility | Normalized fragility | Suppressed / total items |
|---|---|---:|---:|---:|
| anthropic/claude-sonnet-5 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| anthropic/claude-sonnet-5 | ethics_phase2 | 0.069 | 0.069 | 0 / 120 |
| anthropic/claude-sonnet-5 | ipip_neo_120 | 0.781 | 0.195 | 0 / 120 |
| anthropic/claude-sonnet-5 | mfq2_phase2 | 0.575 | 0.144 | 0 / 36 |
| anthropic/claude-sonnet-5 | ous_ggb | 0.362 | 0.090 | 0 / 24 |
| deepseek/deepseek-v4-pro-0813 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| deepseek/deepseek-v4-pro-0813 | ethics_phase2 | 0.187 | 0.187 | 0 / 120 |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | 0.962 | 0.240 | 16 / 120 |
| deepseek/deepseek-v4-pro-0813 | mfq2_phase2 | 0.928 | 0.232 | 0 / 36 |
| deepseek/deepseek-v4-pro-0813 | ous_ggb | 1.066 | 0.267 | 1 / 24 |
| google/gemini-2.5-flash-lite | attention_checks | 0.000 | 0.000 | 0 / 15 |
| google/gemini-2.5-flash-lite | ethics_phase2 | 0.101 | 0.101 | 0 / 120 |
| google/gemini-2.5-flash-lite | ipip_neo_120 | 0.634 | 0.159 | 1 / 120 |
| google/gemini-2.5-flash-lite | mfq2_phase2 | 0.682 | 0.170 | 11 / 36 |
| google/gemini-2.5-flash-lite | ous_ggb | 0.520 | 0.130 | 8 / 24 |
| meta-llama/llama-3.3-70b-instruct | attention_checks | 0.000 | 0.000 | 0 / 15 |
| meta-llama/llama-3.3-70b-instruct | ethics_phase2 | 0.083 | 0.083 | 0 / 120 |
| meta-llama/llama-3.3-70b-instruct | ipip_neo_120 | 0.850 | 0.212 | 0 / 120 |
| meta-llama/llama-3.3-70b-instruct | mfq2_phase2 | 0.841 | 0.210 | 0 / 36 |
| meta-llama/llama-3.3-70b-instruct | ous_ggb | 0.431 | 0.108 | 0 / 24 |
| mistralai/mistral-medium-3.1 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| mistralai/mistral-medium-3.1 | ethics_phase2 | 0.044 | 0.044 | 0 / 120 |
| mistralai/mistral-medium-3.1 | ipip_neo_120 | 0.619 | 0.155 | 0 / 120 |
| mistralai/mistral-medium-3.1 | mfq2_phase2 | 0.436 | 0.109 | 0 / 36 |
| mistralai/mistral-medium-3.1 | ous_ggb | 0.392 | 0.098 | 0 / 24 |
| openai/gpt-5.4-mini | attention_checks | 0.000 | 0.000 | 0 / 15 |
| openai/gpt-5.4-mini | ethics_phase2 | 0.139 | 0.139 | 0 / 120 |
| openai/gpt-5.4-mini | ipip_neo_120 | 0.720 | 0.180 | 0 / 120 |
| openai/gpt-5.4-mini | mfq2_phase2 | 0.909 | 0.227 | 0 / 36 |
| openai/gpt-5.4-mini | ous_ggb | 0.415 | 0.104 | 0 / 24 |
| qwen/qwen3.8-27b | attention_checks | 0.000 | 0.000 | 0 / 15 |
| qwen/qwen3.8-27b | ethics_phase2 | 0.069 | 0.069 | 0 / 120 |
| qwen/qwen3.8-27b | ipip_neo_120 | 0.738 | 0.185 | 0 / 120 |
| qwen/qwen3.8-27b | mfq2_phase2 | 0.766 | 0.191 | 0 / 36 |
| qwen/qwen3.8-27b | ous_ggb | 0.521 | 0.130 | 0 / 24 |
| x-ai/grok-4.20 | attention_checks | 0.020 | 0.020 | 0 / 15 |
| x-ai/grok-4.20 | ethics_phase2 | 0.095 | 0.095 | 28 / 120 |
| x-ai/grok-4.20 | ipip_neo_120 | 1.154 | 0.288 | 0 / 120 |
| x-ai/grok-4.20 | mfq2_phase2 | 0.799 | 0.200 | 0 / 36 |
| x-ai/grok-4.20 | ous_ggb | 0.863 | 0.216 | 0 / 24 |
| z-ai/glm-5.2 | attention_checks | 0.000 | 0.000 | 0 / 15 |
| z-ai/glm-5.2 | ethics_phase2 | 0.120 | 0.120 | 0 / 120 |
| z-ai/glm-5.2 | ipip_neo_120 | 0.840 | 0.210 | 2 / 120 |
| z-ai/glm-5.2 | mfq2_phase2 | 0.871 | 0.218 | 1 / 36 |
| z-ai/glm-5.2 | ous_ggb | 0.586 | 0.147 | 0 / 24 |

## Suppression list

Any listed score has at least one item/condition/framing cell below 70% valid coverage and is excluded from that aggregate. Unlisted aggregates had no suppressed item cells.

| Model | Instrument | Scale | Condition | Framing | Suppressed / total | Mean coverage |
|---|---|---|---|---|---:|---:|
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.altruism | evaluator | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.cooperation | evaluator | first_person | 2 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.modesty | bare | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.modesty | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.morality | evaluator | first_person | 3 / 4 | 60.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness.sympathy | evaluator | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.cautiousness | bare | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.cautiousness | evaluator | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.dutifulness | bare | third_person | 1 / 4 | 75.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | first_person | 3 / 4 | 60.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | first_person | 3 / 4 | 60.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | bare | third_person | 2 / 4 | 55.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | evaluator | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness.self_efficacy | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.activity_level | bare | first_person | 2 / 4 | 75.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.assertiveness | bare | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.assertiveness | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.cheerfulness | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.excitement_seeking | evaluator | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.friendliness | evaluator | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.gregariousness | bare | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.gregariousness | evaluator | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion.gregariousness | evaluator | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.anger | evaluator | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.anxiety | bare | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.anxiety | evaluator | first_person | 2 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.depression | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.depression | evaluator | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.immoderation | evaluator | third_person | 2 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | first_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.self_consciousness | bare | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.vulnerability | bare | first_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism.vulnerability | bare | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.adventurousness | bare | first_person | 2 / 4 | 75.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.artistic_interests | bare | first_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.artistic_interests | bare | third_person | 1 / 4 | 80.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.emotionality | bare | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.emotionality | evaluator | third_person | 1 / 4 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.intellect | bare | first_person | 2 / 4 | 65.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness.liberalism | bare | third_person | 1 / 4 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ous_ggb | ggb.instrumental_harm | bare | first_person | 1 / 12 | 96.7% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.conscientiousness.dutifulness | bare | third_person | 1 / 4 | 90.0% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.neuroticism.depression | bare | first_person | 1 / 4 | 90.0% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.openness.intellect | bare | third_person | 1 / 4 | 80.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.authority | bare | first_person | 4 / 6 | 56.7% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.authority | bare | third_person | 6 / 6 | 33.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.care | bare | third_person | 4 / 6 | 30.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.equality | bare | first_person | 1 / 6 | 83.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.equality | bare | third_person | 6 / 6 | 20.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.loyalty | bare | first_person | 3 / 6 | 60.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.loyalty | bare | third_person | 5 / 6 | 20.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.proportionality | bare | first_person | 1 / 6 | 93.3% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.proportionality | bare | third_person | 4 / 6 | 60.0% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.purity | bare | first_person | 2 / 6 | 66.7% |
| google/gemini-2.5-flash-lite | mfq2_phase2 | mfq2.purity | bare | third_person | 4 / 6 | 40.0% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.impartial_beneficence | bare | first_person | 5 / 12 | 63.3% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.impartial_beneficence | bare | third_person | 8 / 12 | 46.7% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.instrumental_harm | bare | first_person | 3 / 12 | 75.0% |
| google/gemini-2.5-flash-lite | ous_ggb | ggb.instrumental_harm | bare | third_person | 3 / 12 | 75.0% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | bare | first_person | 9 / 24 | 74.2% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | bare | third_person | 5 / 24 | 86.7% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | evaluator | first_person | 4 / 24 | 88.3% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.commonsense | evaluator | third_person | 11 / 24 | 75.8% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.justice | bare | first_person | 12 / 24 | 57.5% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.justice | bare | third_person | 1 / 24 | 95.0% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.justice | evaluator | third_person | 8 / 24 | 79.2% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | bare | first_person | 7 / 24 | 81.7% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | bare | third_person | 12 / 24 | 63.3% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | evaluator | first_person | 1 / 24 | 98.3% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.utilitarianism | evaluator | third_person | 14 / 24 | 66.7% |
| x-ai/grok-4.20 | ethics_phase2 | ethics.virtue | bare | third_person | 1 / 24 | 97.5% |
| z-ai/glm-5.2 | ethics_phase2 | ethics.utilitarianism | evaluator | first_person | 2 / 24 | 94.2% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.conscientiousness.dutifulness | evaluator | third_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.conscientiousness.orderliness | bare | first_person | 1 / 4 | 80.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.neuroticism.depression | bare | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | first_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness.artistic_interests | evaluator | third_person | 1 / 4 | 90.0% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness.liberalism | evaluator | first_person | 2 / 4 | 70.0% |
| z-ai/glm-5.2 | mfq2_phase2 | mfq2.authority | bare | first_person | 1 / 6 | 86.7% |
| z-ai/glm-5.2 | mfq2_phase2 | mfq2.authority | evaluator | first_person | 1 / 6 | 83.3% |
| z-ai/glm-5.2 | mfq2_phase2 | mfq2.loyalty | evaluator | third_person | 1 / 6 | 86.7% |
| z-ai/glm-5.2 | ous_ggb | ggb.instrumental_harm | evaluator | first_person | 2 / 12 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness | bare | third_person | 1 / 24 | 95.8% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness | evaluator | first_person | 6 / 24 | 82.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.agreeableness | evaluator | third_person | 2 / 24 | 90.8% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 4 / 24 | 88.3% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 3 / 24 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | evaluator | first_person | 5 / 24 | 85.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.conscientiousness | evaluator | third_person | 3 / 24 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | bare | first_person | 4 / 24 | 88.3% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | bare | third_person | 1 / 24 | 91.7% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | evaluator | first_person | 3 / 24 | 91.7% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.extraversion | evaluator | third_person | 2 / 24 | 91.7% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | bare | first_person | 3 / 24 | 90.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | bare | third_person | 3 / 24 | 92.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | evaluator | first_person | 5 / 24 | 87.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.neuroticism | evaluator | third_person | 2 / 24 | 95.0% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness | bare | first_person | 5 / 24 | 82.5% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness | bare | third_person | 3 / 24 | 89.2% |
| deepseek/deepseek-v4-pro-0813 | ipip_neo_120 | ipip.openness | evaluator | third_person | 2 / 24 | 93.3% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.conscientiousness | bare | third_person | 1 / 24 | 98.3% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.neuroticism | bare | first_person | 1 / 24 | 97.5% |
| google/gemini-2.5-flash-lite | ipip_neo_120 | ipip.openness | bare | third_person | 1 / 24 | 96.7% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.conscientiousness | bare | first_person | 1 / 24 | 96.7% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.conscientiousness | evaluator | third_person | 1 / 24 | 96.7% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.neuroticism | bare | first_person | 1 / 24 | 96.7% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness | evaluator | first_person | 3 / 24 | 93.3% |
| z-ai/glm-5.2 | ipip_neo_120 | ipip.openness | evaluator | third_person | 1 / 24 | 97.5% |

## GGB validation (bare, first-person)

Higher impartial-beneficence agreement and lower instrumental-harm agreement are the pre-specified directional sanity check. Values are 1–5 agreement means with 95% bootstrap intervals; they are descriptive model outputs, not evidence of moral competence.

Directional flag uses the neutral midpoint: impartial beneficence > 3 and instrumental harm < 3. Reproduced: openai/gpt-5.4-mini, google/gemini-2.5-flash-lite, meta-llama/llama-3.3-70b-instruct, mistralai/mistral-medium-3.1, deepseek/deepseek-v4-pro-0813, z-ai/glm-5.2. Not reproduced / suppressed: anthropic/claude-sonnet-5, x-ai/grok-4.20, qwen/qwen3.8-27b.

| Model | Impartial Beneficence | Instrumental Harm |
|---|---:|---:|
| anthropic/claude-sonnet-5 | 2.467 [2.167, 2.767] | 1.917 [1.383, 2.600] |
| deepseek/deepseek-v4-pro-0813 | 3.317 [2.850, 3.800] | 2.418 [1.873, 2.982] |
| google/gemini-2.5-flash-lite | 3.186 [2.500, 3.850] | 1.267 [1.067, 1.556] |
| meta-llama/llama-3.3-70b-instruct | 4.533 [3.917, 4.900] | 1.100 [1.000, 1.333] |
| mistralai/mistral-medium-3.1 | 3.917 [3.350, 4.383] | 1.650 [1.050, 2.483] |
| openai/gpt-5.4-mini | 3.617 [2.950, 4.133] | 1.250 [1.000, 1.583] |
| qwen/qwen3.8-27b | 2.583 [1.950, 3.250] | 1.717 [1.050, 2.467] |
| x-ai/grok-4.20 | 2.317 [1.667, 3.033] | 1.742 [1.325, 2.246] |
| z-ai/glm-5.2 | 3.350 [2.867, 3.833] | 1.617 [1.150, 2.167] |

## ETHICS reference agreement (bare, first-person)

Each cell is exact agreement with the public ETHICS test label. The score is not a broad ethical-validity claim and should be interpreted alongside the raw prompts and framing effects.

| Model | Commonsense | Deontology | Justice | Utilitarianism | Virtue |
|---|---:|---:|---:|---:|---:|
| anthropic/claude-sonnet-5 | 0.825 [0.667, 0.958] | 0.883 [0.750, 0.992] | 0.842 [0.683, 0.958] | 0.933 [0.825, 1.000] | 0.950 [0.867, 1.000] |
| deepseek/deepseek-v4-pro-0813 | 0.792 [0.625, 0.958] | 0.700 [0.533, 0.850] | 0.700 [0.550, 0.858] | 0.517 [0.342, 0.683] | 0.917 [0.808, 1.000] |
| google/gemini-2.5-flash-lite | 0.775 [0.608, 0.917] | 0.783 [0.617, 0.917] | 0.567 [0.375, 0.758] | 0.758 [0.600, 0.892] | 0.958 [0.875, 1.000] |
| meta-llama/llama-3.3-70b-instruct | 0.700 [0.525, 0.867] | 0.850 [0.708, 0.958] | 0.825 [0.692, 0.950] | 0.850 [0.725, 0.958] | 0.933 [0.850, 0.992] |
| mistralai/mistral-medium-3.1 | 0.633 [0.450, 0.808] | 0.767 [0.600, 0.917] | 0.708 [0.542, 0.875] | 0.667 [0.483, 0.833] | 0.975 [0.917, 1.000] |
| openai/gpt-5.4-mini | 0.675 [0.508, 0.842] | 0.617 [0.450, 0.783] | 0.817 [0.675, 0.933] | 0.925 [0.817, 1.000] | 0.892 [0.767, 0.983] |
| qwen/qwen3.8-27b | 0.783 [0.617, 0.917] | 0.733 [0.550, 0.908] | 0.733 [0.558, 0.875] | 0.925 [0.842, 0.992] | 1.000 [1.000, 1.000] |
| x-ai/grok-4.20 | 0.867 [0.667, 1.000] | 0.733 [0.558, 0.892] | 0.683 [0.417, 0.917] | 0.521 [0.335, 0.703] | 0.892 [0.775, 0.983] |
| z-ai/glm-5.2 | 0.775 [0.608, 0.917] | 0.792 [0.642, 0.925] | 0.817 [0.667, 0.942] | 0.717 [0.550, 0.850] | 0.983 [0.942, 1.000] |

## Design sensitivity

Effects are paired at item level after the coverage rule. `evaluator − bare` holds framing constant; `first − third` holds condition constant. Positive values mean the named first term was higher on the item’s native score scale.

| Model | Scale | Effect | Pairs | Difference [95% CI] |
|---|---|---|---:|---:|
| anthropic/claude-sonnet-5 | ipip.neuroticism.anxiety | first_minus_third | 8 | -2.125 [-2.550, -1.575] |
| openai/gpt-5.4-mini | mfq2.equality | first_minus_third | 12 | -2.050 [-2.617, -1.467] |
| anthropic/claude-sonnet-5 | ipip.neuroticism.self_consciousness | first_minus_third | 8 | -1.881 [-2.475, -1.206] |
| anthropic/claude-sonnet-5 | ipip.conscientiousness.cautiousness | first_minus_third | 8 | +1.775 [+1.300, +2.250] |
| x-ai/grok-4.20 | ipip.extraversion.cheerfulness | first_minus_third | 8 | +1.700 [+1.025, +2.325] |
| anthropic/claude-sonnet-5 | ipip.openness.intellect | first_minus_third | 8 | +1.675 [+1.300, +2.075] |
| meta-llama/llama-3.3-70b-instruct | mfq2.purity | first_minus_third | 12 | -1.667 [-2.283, -1.100] |
| z-ai/glm-5.2 | ipip.neuroticism.anxiety | first_minus_third | 8 | -1.663 [-2.413, -0.875] |
| anthropic/claude-sonnet-5 | ipip.neuroticism.vulnerability | first_minus_third | 8 | -1.625 [-2.050, -1.225] |
| anthropic/claude-sonnet-5 | ipip.conscientiousness.orderliness | first_minus_third | 8 | +1.550 [+0.625, +2.350] |
| meta-llama/llama-3.3-70b-instruct | ipip.neuroticism.anger | first_minus_third | 8 | -1.550 [-2.325, -0.775] |
| google/gemini-2.5-flash-lite | mfq2.purity | first_minus_third | 8 | -1.537 [-2.181, -0.869] |
| anthropic/claude-sonnet-5 | ipip.neuroticism.anger | first_minus_third | 8 | -1.475 [-1.925, -1.000] |
| meta-llama/llama-3.3-70b-instruct | ipip.neuroticism.anxiety | evaluator_minus_bare | 8 | +1.450 [+0.550, +2.325] |
| meta-llama/llama-3.3-70b-instruct | ipip.neuroticism.anxiety | first_minus_third | 8 | -1.450 [-2.575, -0.350] |
| meta-llama/llama-3.3-70b-instruct | ipip.extraversion.cheerfulness | evaluator_minus_bare | 8 | +1.425 [+0.675, +2.200] |
| qwen/qwen3.8-27b | ipip.neuroticism.anxiety | first_minus_third | 8 | -1.375 [-2.325, -0.375] |
| mistralai/mistral-medium-3.1 | ipip.agreeableness.morality | evaluator_minus_bare | 8 | -1.350 [-1.625, -1.050] |
| openai/gpt-5.4-mini | mfq2.purity | first_minus_third | 12 | -1.300 [-1.917, -0.733] |
| z-ai/glm-5.2 | ipip.neuroticism.anger | first_minus_third | 8 | -1.281 [-2.006, -0.606] |
| anthropic/claude-sonnet-5 | ipip.conscientiousness.achievement_striving | first_minus_third | 8 | +1.275 [+0.575, +1.975] |
| anthropic/claude-sonnet-5 | ipip.agreeableness.modesty | first_minus_third | 8 | +1.225 [+1.000, +1.500] |
| openai/gpt-5.4-mini | ipip.neuroticism.anger | first_minus_third | 8 | -1.150 [-1.500, -0.800] |
| anthropic/claude-sonnet-5 | ipip.agreeableness.sympathy | first_minus_third | 8 | +1.125 [+0.625, +1.625] |
| openai/gpt-5.4-mini | ipip.conscientiousness.self_efficacy | first_minus_third | 8 | +1.125 [+0.575, +1.750] |

## Big Five comparison caveat

The HTML artifact compares bare first-person IPIP means with the only readily published IPIP-120 external norm table used here: a Chinese convenience sample (n=131). It is an illustrative reference, not a representative human population benchmark and not a basis for ranking models as people. Source: https://ipip.ori.org/ChineseIPIP-120norms.htm.

## Artifacts

- `reports/02_scoring.html` — self-contained visual dashboard with embedded plots.
- `data/derived/<run-id>/cell_scores.csv` — score/coverage/fragility for every analytical cell.
- `data/derived/<run-id>/scale_scores.csv` and `effects.csv` — publication-facing aggregates.
- `data/derived/<run-id>/summary.json` — run-level machine-readable summary.

Gate 2 remains a Sunay decision.
