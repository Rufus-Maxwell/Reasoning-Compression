# Reasoning Compression

We know AI models often think for too long. They get stuck in reasoning loops, repeat themselves and waste tokens unnecessarily.

**We want to fix that.**

This project explores how to make AI models more efficient by reducing wasted reasoning, cutting unnecessary token usage and maintaining comparable accuracy.

The goal is simple: **get the same quality of answers with less computation.**

## The Project

**LeanReasoning** is the name of our reasoning-compressed Qwen3-1.7B model.

We studied Qwen3-1.7B, a small open-weight reasoning model, using mathematical problems to measure how accurately and efficiently it works.

By examining where the model wastes time and tokens, we identified opportunities to shorten its reasoning through targeted fine-tuning.

We compared the original model against fine-tuned versions under standard and concise prompts, measuring both the efficiency gains and the effect on answer quality.

## Why It Matters

Every unnecessary token takes time and computing power to generate. Across thousands or millions of AI requests, those inefficiencies add up.

If we can make models reason more efficiently while retaining their capabilities, we can reduce processing time, computational demand and the cost of running AI systems.

This independent study is inspired by UkisAI's Swift research.

## Results — updated 4 November 2026

**76% fewer thinking tokens. 75% less generation time. Approximately 4× the workload throughput.**

The complete merged model achieved **89% mathematical accuracy**, compared with **90%** for the original standard-prompt baseline (rounded). On the measured 1,800-response workload, generation fell from **12 hours to 2 hours 58 minutes**.

| Configuration | Accuracy | Mean thinking tokens | Batched generation time |
|---|---:|---:|---:|
| Original — standard prompt | 90.11% | 1,940 | 12h 00m |
| Original — concise prompt | 90.22% | 1,036 | 7h 14m |
| Trained — concise, separate adapter | 88.83% | 450 | 4h 25m |
| **Trained — concise, merged model** | **88.83%** | **466** | **2h 58m** |

Training adds value beyond the concise instruction alone: the merged trained model used **55% fewer thinking tokens and 59% less generation time** than the original model with the same concise prompt.

Each row covers the same **600 final-evaluation questions × three sampled responses**. The merged row is a fresh-seed repeat using the same trained checkpoint, exported and reloaded as a complete model. The original-model controls are retained from the first final evaluation.

The exact accuracy difference against the standard baseline is **1.28 percentage points**. We describe this as substantial efficiency with comparable accuracy and a modest observed trade-off; unchanged accuracy has not been established. Generation times measure batched workloads, not individual-request latency.

[Read the full results, methodology and supporting diagnostics](docs/project-report-2026-11-04.md).

## From shorter reasoning to faster deployment

**V1 — Reasoning compression:** targeted fine-tuning and concise prompting reduced the original workload from 12 hours to 4h 25m.

**V2 — Deployment optimisation:** incorporating the learned adapter into the model weights reduced that workload further to 2h 58m. This produced a standalone model that loads without a separately executed adapter.

The final merged run completed all 1,800 responses with **no token-cap truncations**. Exported weights were verified, reloaded and used for the evaluation.

## Practical impact

The measured reduction saves approximately **nine GPU generation hours per 1,800 responses**. At a fixed GPU rental rate, shorter runtime means lower generation-time cost. It also offers potential electricity savings; energy consumption was not directly measured in this study.

At the observed mean lengths, 10,000 similar responses would avoid approximately **14.7 million thinking tokens**. This is an illustrative extrapolation from the evaluation.

## How it works

We trained two small LoRA variants using **20 selected positive traces and five optimiser updates** each. One used ordinary fine-tuning; the other added a small contextual penalty at **20 annotated positions across 10 questions**. The project owner reviewed these annotations.

The penalty targets unwanted continuations in specific contexts, rather than globally banning words such as “wait” or “alternatively”. Development evaluation compared six training/prompt configurations before selecting the final model.

Correctness uses pinned **Hugging Face Math-Verify 0.9.0** on final answers. The frozen generation protocol uses boxed answers, thinking mode, temperature 0.6, top-p 0.95, top-k 20 and an 8,192-token allowance. Experiments ran on a single RTX 3090.

The [full report](docs/project-report-2026-11-04.md) includes training details, accuracy uncertainty, individual-response timing, the merge diagnostic and failure-retry findings.

## Current status

- Baseline, training and development comparisons: complete.
- Original final evaluation: complete, 5,400 responses.
- Individual-response timing and adapter-merge diagnostic: complete.
- Full merged-model evaluation: complete, 1,800 new responses.
- Standalone model export: complete and verified.
- Project report: available; public model packaging and release remain.

## Research files and history

The [5 November Stage 8 snapshot](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/stage8-results-2026-11-05_13-37) contains the latest evidence and launchers, with original folder paths and a SHA-256 manifest. Full merged model weights remain in the local export pending publication.

The [26 October research snapshot](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/research-update-20261026T171315Z-975570) contains selected source, configurations, data and results available at that date. It predates the completed final evaluation and Stage 8 measurements.

Superseded experiments are preserved as stage-organised ZIP attachments under [Releases](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases), with original folder structures and file manifests. The [1 November research snapshot](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/research-2026-11-01_12-03) preserves the newer source, results, training checkpoints and project downloads with original paths and SHA-256 hashes. Its index distinguishes archived-only files, retained active inputs and files moved into the project. The associated cleanup was applied only after downloading and verifying every uploaded archive.

This repository is the main project page. The original study plan is retained as historical planning material; this page describes the work actually completed.
