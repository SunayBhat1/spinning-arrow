# 21-model launch preflight

**Status:** passed before collection
**Recorded gate:** `data/preflight/20260831T055903Z__phase2.json`
**Panel:** 21 models; 315 fixed items; 6,300 planned calls per model; 132,300 total calls
**Forecast:** `$18.528174` against the user-approved `$20.00` maximum forecast and hard run cap
**Probe cost:** `$0.000776035`

## What this gate verifies

Each candidate received a live, short-answer probe using the exact main-battery configuration:
temperature zero, an eight-token answer allowance, and disabled reasoning (or an explicitly
omitted unsupported reasoning parameter). A candidate entered the full battery only when it:

1. returned a valid answer letter in the required strict format;
2. returned an auditable OpenRouter usage/cost record; and
3. reported **zero** reasoning tokens.

All 21 final-panel candidates passed all three checks. The full runner repeats the same gate before
creating its raw-response directory, and aborts if a main-battery completion reports reasoning
tokens or would exceed its cost reservation.

## Collection recovery

The default-routed Mistral Small collection was stopped after an OpenRouter response omitted its
usage block. That response, and every other response without auditable cost, was excluded rather
than silently priced at zero. The model's partial slice was recollected through `deepinfra`, with
OpenRouter fallback disabled, after the fresh full-panel gate at
`data/preflight/20260831T071029Z__phase2.json`. The completed manifest records this provider
preference and the final run has 132,300 costed records with zero billed reasoning tokens.

## Cleared panel

| Lab | OpenRouter model ID |
|---|---|
| Anthropic | `anthropic/claude-sonnet-5` |
| Amazon | `amazon/nova-lite-v1` |
| DeepSeek | `deepseek/deepseek-v4-pro-0813`, `deepseek/deepseek-v4-flash-0731` |
| Google | `google/gemini-2.5-flash-lite`, `google/gemini-2.5-flash`, `google/gemma-3-27b-it` |
| Meta | `meta-llama/llama-3.1-70b-instruct`, `meta-llama/llama-3.1-8b-instruct` |
| Microsoft | `microsoft/phi-4` |
| Mistral | `mistralai/mistral-medium-3.1`, `mistralai/mistral-small-3.2-24b-instruct` |
| NVIDIA | `nvidia/nemotron-3.5-lightning` |
| OpenAI | `openai/gpt-5.4-mini`, `openai/gpt-5.6-luna`, `openai/gpt-4o-mini-2024-07-18`, `openai/gpt-4.1-mini` |
| Qwen / Alibaba | `qwen/qwen3.8-27b` |
| xAI | `x-ai/grok-4.20` |
| Z.ai | `z-ai/glm-5.2`, `z-ai/glm-4.5-air` |

## Candidates not admitted

The following are not quietly substituted into the comparable panel:

- `meta-llama/llama-3.3-70b-instruct`, Llama 4 Scout, and Llama 4 Maverick failed the strict
  output-format probe.
- Current Qwen Flash/Plus candidates and Cohere Command R7B were unavailable to this account under
  OpenRouter data-policy routing guardrails; Qwen 2.5 72B did not return an auditable usage block.
- Kimi K2 failed the strict letter-only output requirement.
- Liquid LFM, GPT-OSS, and newer Gemini, Grok, Qwen, and GLM candidates that require reasoning
  remain excluded under the main battery's zero-reasoning comparability rule.

This is an access and configuration decision, not a claim about any excluded model's quality.
