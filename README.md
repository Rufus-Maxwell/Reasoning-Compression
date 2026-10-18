# Reasoning Compression

An ongoing, UkisAI Swift-inspired study using Qwen3-1.7B.

## Objective

Reduce unnecessary reasoning tokens and inference time while preserving
final-answer mathematical accuracy under matched evaluation conditions.

## Evaluation methodology

- Primary correctness metric: Hugging Face Math-Verify.
- Final answers requested using boxed notation.
- Track reasoning tokens, generation time, truncation and malformed outputs.
- Inspect reasoning traces qualitatively to understand failures.

## Progress — 18 October 2026

- Initial aptitude and token-budget investigations completed.
- Evaluator checks and boxed-answer prompt comparison completed.
- Stage 5 baseline collection underway: **600 / 3,600 responses saved**.
- First segment: **200 development questions × 3 responses**.
- Final-answer accuracy: **551 / 600 — 91.8%**.
- Mean reasoning length: **1,630 tokens**.
- Truncation: **4 / 600 — 0.67%**.
- Generation and scoring time: approximately **3 hours 21 minutes**.

These are development-set baseline results, not final benchmark or
compression results. No compression training has been performed yet.

## Next steps

1. Complete the remaining Stage 5 baseline segments.
2. Stage 6: discover reasoning markers associated with unnecessary reasoning.
3. Proceed to intervention and training experiments with matched evaluation.

## Research history

Superseded experiments are preserved as stage-organised ZIP attachments
under [Releases](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases).
They include original folder structures and file manifests.

This repository is the main project page. Active source code and further
results will be added as the study progresses.
