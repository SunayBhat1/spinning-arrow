# Phase 4 site preview

**Status:** local preview ready for review; not publicly deployed.
**Build:** `site/` is a static Astro app prepared from the committed Phase 2 and Phase 3 data.

## Included in the preview

- Mobile-first, quiet wabi-sabi visual system: warm paper, moss, clay, generous spacing, and no
  noisy dashboard chrome.
- Plain-language study introduction and score explanations before detailed statistics.
- Model pages, scale pages, and method pages with progressive disclosure.
- Question-level links to fixed-condition exact model prompts, raw outputs, displayed letters, and
  canonical answer mapping.
- A ten-question human short form that runs entirely in the visitor’s browser. It sends and saves
  no answers, and says clearly that its closest-profile result is not a diagnosis or identity claim.
- GitHub Pages Actions workflow prepared, using the project-site path before a custom domain is
  connected.

## Deliberate limits

The public explorer packages one exact response per model/question under the documented `bare` /
`first_person` / permutation-0 condition, rather than downloading the 37 MB complete Phase 2 raw
archive on a phone. The full durable raw archive remains committed and linked through the project
repository. The form uses a short subset, so its output is an educational proximity comparison—not
a full instrument score.

## Before public deployment

1. Review the visual direction and copy in the local preview.
2. Enable GitHub Pages for `SunayBhat1/spinning-arrow` with **GitHub Actions** as source.
3. Push the reviewed branch to deploy the project-site preview.
4. Add `spinning-arrow.sunaybhat.me` in GitHub, complete the generated verification record, and
   add the Squarespace DNS CNAME. Then switch the workflow’s site URL and base path for the custom
   domain, and enforce HTTPS.
