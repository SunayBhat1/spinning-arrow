# Preflight cost table

Estimate uses tiktoken prompt counts, a 300-token maximum completion per request, and pinned public list prices in `run_pilot.py`. It is deliberately conservative and is separate from actual usage-based spending.

| Model | Item | Condition | Requests | Estimated input/sample | Estimated maximum cost |
|---|---|---|---:|---:|---:|
| gpt-4o-mini | jekyll_hyde | R0 | 12 | 407 | $0.002893 |
| gpt-4o-mini | jekyll_hyde | R1 | 12 | 1044 | $0.004039 |
| gpt-4o-mini | jekyll_hyde | R2 | 12 | 23307 | $0.044113 |
| gpt-4o-mini | jekyll_hyde | p4_contamination | 1 | 165 | $0.000205 |
| gpt-4o-mini | bartleby | R0 | 12 | 397 | $0.002874 |
| gpt-4o-mini | bartleby | R1 | 12 | 1018 | $0.003992 |
| gpt-4o-mini | bartleby | R2 | 12 | 15798 | $0.030595 |
| gpt-4o-mini | bartleby | p4_contamination | 1 | 156 | $0.000203 |
| gpt-4o-mini | ethan_frome | R0 | 12 | 432 | $0.002937 |
| gpt-4o-mini | ethan_frome | R1 | 12 | 1036 | $0.004024 |
| gpt-4o-mini | ethan_frome | R2 | 12 | 23319 | $0.044134 |
| gpt-4o-mini | ethan_frome | p4_contamination | 1 | 152 | $0.000203 |
| gpt-4o-mini | metamorphosis | R0 | 12 | 406 | $0.002889 |
| gpt-4o-mini | metamorphosis | R1 | 12 | 1002 | $0.003962 |
| gpt-4o-mini | metamorphosis | R2 | 12 | 24113 | $0.045562 |
| gpt-4o-mini | metamorphosis | p4_contamination | 1 | 154 | $0.000203 |
| gpt-4.1-mini | jekyll_hyde | R0 | 12 | 407 | $0.007714 |
| gpt-4.1-mini | jekyll_hyde | R1 | 12 | 1044 | $0.010771 |
| gpt-4.1-mini | jekyll_hyde | R2 | 12 | 23307 | $0.117634 |
| gpt-4.1-mini | jekyll_hyde | p4_contamination | 1 | 165 | $0.000546 |
| gpt-4.1-mini | bartleby | R0 | 12 | 397 | $0.007663 |
| gpt-4.1-mini | bartleby | R1 | 12 | 1018 | $0.010644 |
| gpt-4.1-mini | bartleby | R2 | 12 | 15798 | $0.081588 |
| gpt-4.1-mini | bartleby | p4_contamination | 1 | 156 | $0.000542 |
| gpt-4.1-mini | ethan_frome | R0 | 12 | 432 | $0.007832 |
| gpt-4.1-mini | ethan_frome | R1 | 12 | 1036 | $0.010732 |
| gpt-4.1-mini | ethan_frome | R2 | 12 | 23319 | $0.117690 |
| gpt-4.1-mini | ethan_frome | p4_contamination | 1 | 152 | $0.000541 |
| gpt-4.1-mini | metamorphosis | R0 | 12 | 406 | $0.007705 |
| gpt-4.1-mini | metamorphosis | R1 | 12 | 1002 | $0.010566 |
| gpt-4.1-mini | metamorphosis | R2 | 12 | 24113 | $0.121499 |
| gpt-4.1-mini | metamorphosis | p4_contamination | 1 | 154 | $0.000542 |

**Final estimate:** $0.707037; **hard cap:** $5.00.
