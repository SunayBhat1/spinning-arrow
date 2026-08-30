# Invalid Phase 1 pilot attempt — do not score

This attempt was stopped after 461 checkpointed calls on 2026-08-30. It used the approved
Phase 1 mandatory-reasoning exception for GPT-OSS and Gemini, but retained the standard
eight-token response ceiling. GPT-OSS frequently consumed that allowance before it could emit a
final answer; 372 records therefore have no textual completion and were classified as errors.

The client revision that launched this attempt also released a reservation when content was absent,
so those error records show zero cost despite OpenRouter having returned a usage block. The actual
cost for this discarded partial attempt cannot be reconstructed from the persisted records. It is
excluded from all analysis and from the clean pilot's cost reconciliation.

The raw checkpoint files are retained for auditability. The clean retry uses committed revision
`1b6abdb5183dffba399642cc18a0670e8ad5ef27`, records 64- and 512-token ceilings for the two mandatory-reasoning models, and
settles usage before classifying a contentless completion.
