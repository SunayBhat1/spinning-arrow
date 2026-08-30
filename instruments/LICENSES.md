# Instrument provenance and licenses

## MFQ-2 pilot subset

- **Instrument:** Moral Foundations Questionnaire-2 (MFQ-2), Atari, Graham, Haidt et al. (2023),
  *Moral Foundations Theory: The pragmatic validity of moral pluralism.*
- **Committed subset:** items 1–20 of the 36-item English form, retained in original order. This
  gives four Care and Equality items and three items for each remaining foundation.
- **License:** CC BY 4.0, per the source publication and project decision D3.
- **Citation of record:** https://doi.org/10.1016/j.paid.2023.112499
- **Form checked against:** https://psytests.org/life/mfq2en-bl.html (downloaded 2026-08-29).

## ETHICS deontology pilot subset

- **Instrument:** ETHICS, Hendrycks et al. (2021), *Aligning AI With Shared Human Values*.
- **Committed subset:** 20 records sampled without replacement from the public deontology test
  split using Python's `random.Random(20260829)`, then stored with their source row index.
- **License:** MIT; the source repository's `LICENSE` is reproduced in this project's `NOTICE`.
- **Citation of record:** https://arxiv.org/abs/2008.02275
- **Source checked against:** https://huggingface.co/datasets/hendrycks/ethics (downloaded
  2026-08-29).

No CC BY-NC-SA or non-commercial material is in this pilot bank.

## Phase 2 fixed bank

The full bank is generated once by `scripts/build_phase2_instruments.py`. Its exact source-file
SHA-256 values, selection seed (`20260830`), and resulting inputs are committed in
`instruments/PHASE2_SOURCES.json`; the generator is part of the reviewed codebase. The Phase 1
files above remain unchanged so their approved manifest continues to identify its original bank.

### IPIP-NEO-120

- **Instrument:** Johnson IPIP-NEO-120 (120 public-domain items; four items for each of 30 NEO
  facets), Johnson (2014), *Measuring thirty facets of the Five Factor Model with a 120-item public
  domain inventory*.
- **License:** public domain, as designated by the International Personality Item Pool.
- **Source of record:** https://ipip.ori.org/30FacetNEO-PI-RItems.htm (key page downloaded
  2026-08-30). The broad IPIP-NEO-120 page is also hash-pinned because it was checked during
  source validation.
- **Citation:** https://doi.org/10.1016/j.jrp.2014.05.003

### Full MFQ-2

- **Instrument:** the complete 36-item English MFQ-2 form, preserved in source order.
- **License:** CC BY 4.0, per the project decision D3 and source publication.
- **Source of record:** https://psytests.org/life/mfq2en-bl.html (downloaded 2026-08-30).
- **Citation:** https://doi.org/10.1016/j.paid.2023.112499

### Oxford Utilitarianism Scale / Greatest Good Benchmark

- **Instrument:** 24 statements selected without replacement (12 Impartial Beneficence, 12
  Instrumental Harm) from the public Greatest Good Benchmark data, using the committed seed.
- **Source of record:** https://github.com/noehsueh/greatest-good-benchmark/blob/main/data/GreatestGoodBenchmark.json
- **Citation:** https://arxiv.org/abs/2505.18836
- **License:** MIT, per the source repository.

### ETHICS test splits

- **Instrument:** 120 records, 24 deterministic records per public ETHICS test split:
  commonsense, deontology, justice, virtue, and utilitarianism.
- **License:** MIT; the source repository's MIT notice is reproduced in this project's `NOTICE`.
- **Source of record:** https://huggingface.co/datasets/hendrycks/ethics and
  https://github.com/hendrycks/ethics (downloaded 2026-08-30).
- **Citation:** https://arxiv.org/abs/2008.02275

### Attention checks

- **Instrument:** 15 project-authored, explicit response-format checks. They contain no sourced
  questionnaire material and are scored only as response-quality checks, not as psychological or
  moral measures.
