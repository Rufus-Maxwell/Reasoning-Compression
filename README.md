# Reasoning Compression

We know AI models often think for too long. They get stuck in reasoning loops, repeat themselves and waste tokens unnecessarily.

**We want to fix that.**

This project explores how to make AI models more efficient by reducing wasted reasoning, cutting unnecessary token usage and maintaining comparable accuracy.

The goal is simple: **get the same quality of answers with less computation.**

## The Project

We studied Qwen3-1.7B, a small open-weight reasoning model, using mathematical problems to measure how accurately and efficiently it works.

By examining where the model wastes time and tokens, we identified opportunities to shorten its reasoning through targeted fine-tuning.

We compared the original model against fine-tuned versions under standard and concise prompts, measuring both the efficiency gains and the effect on answer quality.

## Why It Matters

Every unnecessary token takes time and computing power to generate. Across thousands or millions of AI requests, those inefficiencies add up.

If we can make models reason more efficiently while retaining their capabilities, we can reduce processing time, computational demand and the cost of running AI systems.

This independent study is inspired by UkisAI's Swift research.

## Results — updated 1 November 2026

**The selected trained model with concise prompting used 76.8% fewer thinking tokens and 63.1% less batched generation time than the original model with the standard prompt.** Final-answer accuracy was **88.8% versus 90.1%**, a decrease of **1.28 percentage points**.

This is a substantial efficiency improvement with a modest observed accuracy trade-off. It does not establish unchanged or statistically equivalent accuracy.

### Final held-out evaluation

The configuration was selected using development results before this evaluation. Each row covers the same **600 held-out questions × 3 sampled responses**, giving 1,800 responses per configuration and **5,400 responses overall**. Repeated responses to a question are grouped observations, not 1,800 independent questions.

| Configuration | Correct | Accuracy | Mean thinking tokens | Batched generation time | Truncated |
|---|---:|---:|---:|---:|---:|
| Original, standard prompt | 1,622/1,800 | 90.11% | 1,940 | 12.00 hours | 36 |
| Original, concise prompt | 1,624/1,800 | 90.22% | 1,036 | 7.24 hours | 13 |
| Targeted-penalty fine-tuning, concise prompt | 1,599/1,800 | 88.83% | 450 | 4.42 hours | 1 |

The headline comparison changes both training and prompting. Against the **original model with the same concise prompt**, the trained configuration used **56.6% fewer thinking tokens** and **38.9% less generation time**, with accuracy **1.39 percentage points lower**. On matched responses, 55 answers became correct and 80 became incorrect.

Batched generation times measure the full generation workload, not individual request latency, training time or model-loading time. All three configurations used the same frozen scoring and generation protocol.

### Individual response timing

A separate Stage 8 run measured batch-size-one generation on **200 development questions**, with one response per question and configuration. These are supplementary timing measurements, not a replacement for the held-out accuracy results above.

| Configuration | Correct | Mean thinking tokens | Mean generation time | Median | 95th percentile |
|---|---:|---:|---:|---:|---:|
| Original, standard prompt | 185/200 | 1,586 | 36.2 s | 27.2 s | 86.2 s |
| Original, concise prompt | 185/200 | 813 | 19.5 s | 14.2 s | 51.5 s |
| Targeted-penalty fine-tuning, concise prompt | 187/200 | 346 | 15.6 s | 12.9 s | 34.0 s |

The trained combination reduced mean generation time by **56.8%** versus the original standard configuration and **19.8%** versus concise prompting alone. Timings include prompt processing and decoding, but exclude model loading, tokenisation, queueing and network/UI overhead.

The trained adapter's lower measured token throughput prompted a separate-versus-merged LoRA deployment diagnostic. **That diagnostic is prepared but has not yet produced results.** The cause of the throughput difference remains unconfirmed.

## Evaluation methodology

- One primary correctness metric: final-answer mathematical accuracy using pinned **Hugging Face Math-Verify 0.9.0**. Internal reasoning that contains the right answer does not override an incorrect final answer.
- Final answers requested using boxed notation.
- Frozen Qwen3 thinking-mode sampling: temperature 0.6, top-p 0.95, top-k 20 and an 8,192-token generation limit.
- Matched questions, prompts and sampling schedules for each relevant comparison; development and final question partitions are disjoint.
- Report thinking/output tokens, measured generation time, truncation and malformed responses alongside accuracy.
- Inspect reasoning traces qualitatively to distinguish useful checking from repetition and unsupported reinterpretation.
- Experiments ran on a single RTX 3090. Performance figures describe this model, hardware and inference implementation.

## Training and configuration selection

Two LoRA variants were trained: ordinary cross-entropy fine-tuning and the same fine-tuning with a small contextual unlikelihood penalty. The pilot used **20 selected positive traces**, **20 annotated negative positions across 10 questions**, and **five optimiser updates** per variant.

The penalty targets a particular next token in an annotated context. It is **not a blanket ban** on words such as “wait”, “but” or “alternatively”; those can also introduce useful checks. The annotations were reviewed by the project owner.

Following the initial 20-question pilot, the expanded development evaluation used **200 questions × 3 responses across six configurations**:

| Configuration | Correct / 600 | Mean thinking tokens |
|---|---:|---:|
| Original, standard prompt | 551 | 1,630 |
| Original, concise prompt | 557 | 743 |
| Ordinary fine-tuning, standard prompt | 554 | 744 |
| Ordinary fine-tuning, concise prompt | 554 | 369 |
| Targeted-penalty fine-tuning, standard prompt | 553 | 657 |
| Targeted-penalty fine-tuning, concise prompt | 554 | 348 |

The targeted-penalty variant with concise prompting was selected for final evaluation. Its initial pilot disadvantage did not persist in the expanded development totals, but the held-out evaluation subsequently showed the accuracy trade-off reported above.

This remains a small-scale study with a deliberately limited training budget. Reinforcement learning, on-policy distillation, larger-model validation and extensive penalty optimisation were not completed and are not claimed.

## Current status

- Baseline, training pilot and expanded development evaluation: complete.
- Final held-out evaluation: complete, 5,400 responses.
- Individual response timing: complete, 600 responses.
- Adapter merge diagnostic: prepared; results pending.
- Final report, reproduction documentation and repository organisation: in progress.

## Research files and history

The [26 October research snapshot](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases/tag/research-update-20261026T171315Z-975570) contains selected source, configurations, data and results available at that date. It predates the completed final evaluation and Stage 8 measurements.

Superseded experiments are preserved as stage-organised ZIP attachments under [Releases](https://github.com/Rufus-Maxwell/Reasoning-Compression/releases), with original folder structures and file manifests. The README now reflects the newer verified results; uploading the newer local evidence and performing the associated cleanup are in progress.

This repository is the main project page. The original study plan is retained as historical planning material; this page describes the work actually completed.
