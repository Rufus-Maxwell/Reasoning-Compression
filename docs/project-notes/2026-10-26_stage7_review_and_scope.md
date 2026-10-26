# Stage 7 — Human review and scope decision

Date: 26 October 2026

## Review and authorisation

The project owner authorised the overnight pilot on 25 October before completing the document review, choosing to use the available compute window and review the selections afterwards. On 26 October, the owner confirmed having read `experiments/stage7_pilot/Review.html`, accepted the proposed annotations for this pilot, and approved proceeding.

The original launch acceptance flag records the command used. This note records the subsequent human review; original archives and experiment records remain unchanged.

## What was accepted

The review covers the pilot's 20 positive training examples, 20 contextual penalty positions across 10 discovery questions, and accompanying held-out context assessments. Selected penalty points frequently begin with transitions such as “but”, “wait” and “alternatively”. Acceptance concerns those occurrences in their preceding contexts, not a blanket judgement against these words or against useful self-correction.

## Scope decision

Keep the current pilot approach fixed while expanding matched evaluation of the existing adapters. Avoid an open-ended search over penalty tokens and penalty strengths at this stage. More detailed optimisation may be pursued in a future extension, including work with other models, if justified by available time and compute.

The preliminary combination of concise fine-tuning and concise prompting is sufficiently promising to warrant broader evaluation. This is a decision to proceed, not a claim that accuracy preservation has already been established. Retain the targeted-penalty branch and its observed accuracy trade-off as part of the evidence.

## Next evidence

Compare the trained adapters with the original model under matched standard and concise prompting conditions on a larger development set. Keep final-answer Math-Verify accuracy primary, alongside reasoning/output tokens, generation time, truncation and targeted qualitative inspection. Preserve the final test set for the agreed final evaluation.

## References

- Pilot evidence: `stage7_2026-10-25_21-52.zip`
- Reviewed document: `experiments/stage7_pilot/Review.html`
- [Current project overview and pilot results](../../README.md)
- [Research snapshot uploaded 26 October](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/research-update-20261026T171315Z-975570)

This note documents the owner's explicit decisions in the project conversation. It does not change the master manual, training package, model checkpoints or original results.
