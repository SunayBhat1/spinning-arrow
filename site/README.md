# Spinning Arrow site

This is the static Astro site for the public dashboard. `npm run prepare-data` reads the committed
Phase 2/3 evidence and produces a local build input; raw answer excerpts are deliberately limited
to one fixed, documented response condition so the mobile site remains usable.

## Local preview

```sh
npm install
npm run dev
```

## GitHub Pages

The root workflow builds this directory and deploys it as the repository's project Pages site.
Before using the planned custom domain, set the repository Pages source to **GitHub Actions**, add
`spinning-arrow.sunaybhat.me` in GitHub Pages settings, add the exact verification and CNAME DNS
records GitHub supplies in Squarespace, then set `PUBLIC_SITE_URL` and `PUBLIC_BASE_PATH=/` in the
workflow. Until then, the project site deploys under `/spinning-arrow/`.
