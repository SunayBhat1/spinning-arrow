# Phase 4 site preview

**Status:** local preview ready for review; not publicly deployed.
**Build:** `site/` is a static Astro app prepared from the committed Phase 2 and Phase 3 data.

## Included in the preview

- Mobile-first, quiet wabi-sabi visual system: warm paper, moss, clay, generous spacing, and no
  noisy dashboard chrome.
- Plain-language study introduction and score explanations before detailed statistics.
- Two deliberate browse paths: model-first dossiers and metric-first nine-model comparisons.
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
  scale average. Nothing is sent or saved; the closest-profile result is not a diagnosis or identity
  claim.
- GitHub Pages Actions workflow prepared, using the project-site path before a custom domain is
  connected.

## Deliberate limits

The public explorer packages one exact response per model/question under the documented `bare` /
`first_person` / permutation-0 condition, rather than downloading the 37 MB complete Phase 2 raw
archive on a phone. The full durable raw archive remains committed and linked through the project
repository. The form uses benchmark subsets, so its output is an educational proximity comparison—
not a full instrument score. The currently completed nine-model bank has no technology privacy or
security dilemmas; those must be sourced and run before they can be represented in a comparison.

The present panel has one model per provider and lacks uniformly public, comparable size,
architecture, release-date, and training-cutoff metadata. The new pattern views therefore help
read the measured response data, but they do not estimate factor effects or imply that a provider
caused a result.

## Before public deployment

1. Review the visual direction and copy in the local preview.
2. Enable GitHub Pages for `SunayBhat1/spinning-arrow` with **GitHub Actions** as source.
3. Push the reviewed branch to deploy the project-site preview.
4. Add `spinning-arrow.sunaybhat.me` in GitHub, complete the generated verification record, and
   add the Squarespace DNS CNAME. Then switch the workflow’s site URL and base path for the custom
   domain, and enforce HTTPS.
