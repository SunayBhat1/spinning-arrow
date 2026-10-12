# Bottom line

**The assay runs cheaply and detects differences, but this pilot does not show a general stabilizing effect from richer context.** We completed the predeclared balanced run for **$2.0243 total**, including preliminary format checks and retries. We did not spend the remaining allowance merely to search for a positive result.

## The most useful findings

1. **The average hides opposing model responses.** On the same five stories, full text versus the short vignette changed identical-prompt repeat agreement by +12.7 percentage points for GPT-4o mini, −4.0 for GPT-4.1 mini, +1.7 for Gemini Flash-Lite, and −8.3 for Haiku. Their mean is only +0.5 points. GPT-4o mini improves and Haiku declines in both preassigned three-sample blocks. Gemini's direction reverses between blocks; GPT-4.1 mini is flat within each block despite a small pooled decline. None of the four shows a strictly improving short → synopsis → full-text sequence.

2. **Prompt sensitivity and ordinary randomness are different.** Full-text modal flip rates fall for GPT-4o mini and Gemini, stay unchanged for GPT-4.1 mini, and rise for Haiku compared with short context. Unique-mode denominators are small and differ because ties are excluded. The tie-inclusive bounds and distribution-level comparisons are in `analysis.json`. We should not advertise a pooled flip reduction without this model-level qualification.

3. **Richer context can move the answer, not simply steady it.** In *Enemies*, GPT-4.1 mini and Haiku switch their overall modal action from attending the outside patient to staying with the grieving wife. In *To Build a Fire*, three models' overall modes move toward attempting to kill the dog for warmth; two of those models also become less repeatable. These are changes in response to information or framing, not evidence that either answer is morally better. Eight of the 20 matched model/story combinations change their overall mode between short and full text.

4. **Models converge somewhat without becoming uniformly steadier.** The average pairwise chance that two different models choose the same action on a matched prompt rises from 46.6% with short context to 58.9% with the synopsis and 57.2% with full text. Agreement among models is not the same as repeatability within a model, and neither is correctness.

5. **The apparatus needs refinement before expansion.** All 2,016 first attempts supplied schema-valid decisions, but Haiku had 54 decision jobs still exceeding the 60-word explanation limit after one retry. The all-model plots therefore use an explicitly labeled first-attempt choice-valid sensitivity analysis, not the original fully compliant analysis. The strict analysis confirms the same broad GPT/Gemini directions but leaves no fully complete three-arm Haiku story. Explanation-length compliance should be tracked separately from semantic decisions in the next protocol.

## What the recall checks tell us

The coding assistant's source comparison finds 25 of 32 probes naming the broad author action, while 30 claimed familiarity. Five affirmative claims were wrong about the core action, and even some correct ones included invented details. Two models honestly admitted not knowing *The Three Strangers*; a validator bug unnecessarily retried those empty-description answers, and one retry hallucinated knowledge. The bug is fixed, the cost and original responses remain recorded, and first attempts are used for the recall review. An independent reader should check the annotations.

This makes “the model says it knows the story” an inadequate contamination measure. Conversely, failing the recall probe does not prove the decision response was uncontaminated. Names remain visible, and the assay has no genuinely unfamiliar-story control.

## What we can responsibly conclude

The experiment is feasible at this budget. It provides a useful way to separate repeated-answer variability, sensitivity to harmless prompt changes, and changes of preferred action when new context is added. It does **not** establish that context richness generally “stops the spinning arrow,” nor does it measure real agent behavior or locate a model on a stable moral axis.

The average full-minus-short repeat-agreement difference is tiny; a descriptive bootstrap over just five story clusters spans roughly −2.8 to +4.2 points. That calculation is a sensitivity check, not a defensible population-level confidence claim from five selected literary examples. The richer arms differ in facts, emotional presentation, prior-character behavior, and length. Those cannot yet be separated.

Reasoning was requested disabled, but Gemini reported two reasoning tokens on 50 responses (100 total); this is recorded as a provider-reported deviation rather than silently calling the run entirely non-thinking. No other model reported reasoning tokens.

## Best next experiment

Keep the four inexpensive models and improve the **items**, not merely the repeat count. Have independent readers validate the decision point, the equivalence of action options, and the information contained in each context arm. Repair *Enemies*' awkward referral/transport alternatives and *The Postmaster*'s overlapping B/C packages. Add several unfamiliar or newly written stories, two independently authored summaries per story, and a short version containing the same decision-relevant facts as the long version. Then preregister the comparison and explanation-compliance rule before running. This would test whether narrative richness itself helps, rather than whether one particular summary omitted an important fact.

No production deployment or public moral-ranking claim is warranted from this pilot.
