# Reasoning Compression

We know AI models often think for too long. They get stuck in reasoning loops, repeat themselves and waste tokens unnecessarily.

**We want to fix that.**

This project explores how to make AI models more efficient by reducing wasted reasoning, cutting unnecessary token usage and maintaining comparable accuracy.

The goal is simple: **get the same quality of answers with less computation.**

## The Project

We're starting with Qwen3-1.7B, a small open-source reasoning model, and testing it against mathematical problems to measure how accurately and efficiently it works.

By examining where the model wastes time and tokens, we can identify opportunities to improve its reasoning through training.

We'll compare the original model against modified versions, measuring whether we can reduce unnecessary thinking without sacrificing the quality of its answers.

## Why It Matters

Every unnecessary token takes time and computing power to generate. Across thousands or millions of AI requests, those inefficiencies add up.

If we can make models reason more efficiently while retaining their capabilities, we can reduce processing time, computational demand and the cost of running AI systems.

This independent study is inspired by UkisAI's Swift research.

## Evaluation methodology

- Primary correctness metric: Hugging Face Math-Verify.
- Final answers requested using boxed notation.
- Track reasoning tokens, generation time, truncation and malformed outputs.
- Inspect reasoning traces qualitatively to understand failures.

## Preliminary findings — 26 October 2026

The Stage 7 development pilot compared the original model, ordinary fine-tuning (CE-only), and marker-penalty training under standard and concise prompts. Each configuration used **20 questions × 3 responses**, giving 60 responses per configuration. Correctness is final-answer mathematical accuracy scored using Math-Verify.

| Model | Prompt | Correct responses | Mean thinking tokens | Generation time |
|---|---|---:|---:|---:|
| Original | Standard | 47/60 | 2,033 | 27.0 minutes |
| Ordinary fine-tuning | Standard | 48/60 | 847 | 16.8 minutes |
| Marker-penalty training | Standard | 45/60 | 713 | 12.5 minutes |
| Original | Concise | 48/60 | 911 | 10.5 minutes |
| Ordinary fine-tuning | Concise | 47/60 | 393 | 7.6 minutes |
| Marker-penalty training | Concise | 44/60 | 364 | 6.4 minutes |

**Training and concise prompting combined usefully in this pilot.** Compared with the original model under the standard prompt, ordinary fine-tuning with the concise prompt reduced mean thinking tokens by approximately **80.7% (2,033 → 393)** and generation time by approximately **71.9% (27.0 → 7.6 minutes)**, with the same number of correct responses: **47/60**. This comparison changes both training and prompting; the separate controls are shown above.

Compared with concise prompting alone, ordinary fine-tuning reduced thinking tokens by **56.9% (911 → 393)**, with **47/60 versus 48/60** correct. The marker penalty shortened reasoning further but reduced accuracy more, so it is not currently the preferred approach.

These are preliminary development-pilot results, not final held-out benchmark results or proof of equivalent accuracy. Generation-time comparisons use the rounded times reported above. Larger matched evaluation is needed to establish how reliably these gains generalise.

## Next steps

Expand the matched evaluation of the promising ordinary fine-tuning approach, assess accuracy and efficiency together, and use the findings to guide subsequent interventions. The longer-term project plan includes reinforcement learning and on-policy distillation; these are not claimed as completed here.

## Research files

The [latest research snapshot](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/research-update-20261026T171315Z-975570) contains selected project source, configurations, data and results, plus the identified project downloads where present. Original relative paths and a SHA-256 manifest are included. Model weights, checkpoints, environments, caches, backups, the legacy Swift_Replication_Project folder and the master manual are excluded. Local files are retained.

## Research history

Superseded experiments are preserved as stage-organised ZIP attachments
under [Releases](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases).
They include original folder structures and file manifests.

This repository is the main project page. Active source code and further
results will be added as the study progresses.
