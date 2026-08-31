# Phase 4 site preview

**Status:** publicly deployed at `https://spinning-arrow.sunaybhat.me/`.
**Build:** `site/` is a static Astro app prepared from the completed 21-model launch evidence at
build time.

## Included in the preview

- Mobile-first, quiet wabi-sabi visual system: warm paper, moss, clay, generous spacing, and no
  noisy dashboard chrome.
- Plain-language study introduction and score explanations before detailed statistics.
- Two deliberate browse paths: model-first dossiers and metric-first comparisons across every
  tested model; the current launch panel has 21 profiles.
  The latter show item-resampled intervals and lead to the source prompt and exact response.
- A Patterns page with an interactive metric-to-metric scatter plot, model-to-model item-response
  similarity heatmap, and small-sample-safe readiness views for future provider/lab, size,
  architecture, release-date, and training-cutoff analyses.
- Model pages, scale pages, and method pages with progressive disclosure.
- Question-level links to fixed-condition exact model prompts, raw outputs, displayed letters, and
  canonical answer mapping.
- Two browser-only human response paths: a concise ten-question reflection and a 33-question
  detailed reflection with five context-rich ETHICS cases. Each prompt identifies its source, and
  each comparison uses a model's answer to the same individual questions rather than a broad
  scale average. Results rank the closest five response patterns, plot every tested model, and can
  reveal a selected model’s full same-question comparison with an evidence link for every row.
  Nothing is sent or saved; the closest-profile result is not a diagnosis or identity claim.
- GitHub Pages Actions workflow prepared, using the project-site path before a custom domain is
  connected.

## Deliberate limits

The public explorer packages one exact response per model/question under the documented `bare` /
`first_person` / permutation-0 condition, rather than downloading the 37 MB complete Phase 2 raw
archive on a phone. The full durable raw archive remains committed and linked through the project
repository. The form uses benchmark subsets, so its output is an educational proximity comparison—
not a full instrument score. The currently completed bank has no technology privacy or
security dilemmas; those must be sourced and run before they can be represented in a comparison.

The launch panel contains 21 models and several within-lab model pairs, which supports descriptive comparison
within those labs. It still lacks uniformly public, comparable size, architecture, release-date,
and training-cutoff metadata. The pattern views therefore help read the measured response data, but
they do not estimate factor effects or imply that a provider caused a result.

## Deployment record

GitHub Pages is the static host, with the custom subdomain configured through Squarespace DNS. The
Actions workflow deploys the `main` branch; each completed evidence update is built locally,
committed with its raw/derived provenance, then published through that workflow.
