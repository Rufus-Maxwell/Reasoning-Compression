# Stage 7 — Human review and scope decision

Date: 26 October 2026

## Human review and approval

The project owner has read `experiments/stage7_pilot/Review.html`, accepted the proposed annotations for this pilot, and approved proceeding to broader evaluation.

## What was accepted

The review covers the pilot's 20 positive training examples, 20 contextual penalty positions across 10 discovery questions, and accompanying held-out context assessments. Selected penalty points frequently begin with transitions such as “but”, “wait” and “alternatively”. Acceptance concerns those occurrences in their preceding contexts, not a blanket judgement against these words or against useful self-correction.

## Scope decision

Keep the current pilot approach fixed while expanding matched evaluation of the existing adapters. Avoid an open-ended search over penalty tokens and penalty strengths at this stage.

The preliminary combination of concise fine-tuning and concise prompting is sufficiently promising to warrant broader evaluation. This is a decision to proceed, not a claim that accuracy preservation has already been established. Retain the targeted-penalty branch and its observed accuracy trade-off as part of the evidence.

## Future extension

If the project is expanded, including to larger models, investigate which context-specific tokens and continuations contribute most to unnecessary repetition or reasoning detours. Assess both which occurrences to penalise and how strongly to penalise them, with the aim of preserving more of the original model's accuracy while reducing reasoning cost. Distinguish harmful repetition from useful verification and error correction rather than treating transition words as inherently undesirable.

This more detailed optimisation is deferred to keep the current study focused and proportionate to its scope.

## Next evidence

Compare the trained adapters with the original model under matched standard and concise prompting conditions on a larger development set. Keep final-answer Math-Verify accuracy primary, alongside reasoning/output tokens, generation time, truncation and targeted qualitative inspection. Preserve the final test set for the agreed final evaluation.

## References

- Pilot evidence: `stage7_2026-10-25_21-52.zip`
- Reviewed document: `experiments/stage7_pilot/Review.html`
- [Current project overview and pilot results](../../README.md)
- [Research snapshot uploaded 26 October](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/research-update-20261026T171315Z-975570)

This note documents the owner's review and scope decisions. It does not change the master manual, training package, model checkpoints or original results.
