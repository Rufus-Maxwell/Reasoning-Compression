# Reasoning Compression — project report
Updated 4 November 2026

## Outcome

A small, targeted fine-tuning experiment on Qwen3-1.7B, combined with concise prompting and a merged model export, reduced mean thinking length from **1,940 to 466 tokens** and the measured generation workload from **12 hours to 2 hours 58 minutes**.

That is **76.0% fewer thinking tokens**, **75.3% less generation time**, and approximately **4× the workload throughput**. Final-answer accuracy was **88.83% versus 90.11%** for the original standard-prompt baseline: a 1.28 percentage-point difference.

The project demonstrates a practical route from inspecting inefficient reasoning to training a smaller reasoning footprint and deploying it efficiently on a single RTX 3090. The result, named **LeanReasoning**, is a complete exported model, not only an adapter requiring separate execution.

## What we built

The work had three distinct parts:

1. **Measurement.** Establish a reproducible baseline that distinguishes final-answer correctness, reasoning length and runtime. Early prompt and evaluator problems were investigated before freezing the main protocol.
2. **Reasoning compression.** Train small LoRA updates using selected correct concise traces, with an additional branch penalising specific unwanted continuations in annotated contexts.
3. **Deployment optimisation.** Fold the chosen adapter into the original weights, save the complete model, verify and reload it, and measure the resulting deployment.

Concise prompting alone was an effective control. Training added further savings beyond that control; merging then removed substantial adapter execution overhead.

## Main results

Each row contains 1,800 responses to the same 600 final-evaluation questions, with three sampled responses per question. The first three rows are the original final evaluation. The last row is a fresh-seed deployment repeat on those same questions, using the same trained checkpoint merged into the base model.

| Configuration | Correct / 1,800 | Accuracy | Mean thinking tokens | Generation time | Capped responses |
|---|---:|---:|---:|---:|---:|
| Original — standard prompt | 1,622 | 90.11% | 1,940.07 | 12h 00m 04s | 36 |
| Original — concise prompt | 1,624 | 90.22% | 1,035.91 | 7h 14m 25s | 13 |
| Trained — concise, separate adapter | 1,599 | 88.83% | 449.87 | 4h 25m 22s | 1 |
| Trained — concise, merged model | 1,599 | 88.83% | 466.26 | 2h 58m 10s | 0 |

The merged model used **55.0% fewer thinking tokens and 59.0% less generation time than the original with concise prompting**. Against the separate-adapter deployment, generation time fell by **32.9%**. The merged repeat produced somewhat longer outputs with different sampling seeds, so that last percentage is a measured workload comparison rather than a perfectly isolated measurement of merge overhead.

The two trained runs had the same aggregate accuracy; that does not establish identical answers. All 1,800 merged-run responses included a boxed answer and none reached the 8,192-token cap.

### How time was measured

Main-table times sum generation wall time over batches of four. They exclude training, model loading, export, scoring, archive verification and network/UI overhead. They are **complete-workload measurements, not individual-request latency**.

The merged run generated 1,052,210 output tokens at an aggregate **98.43 tokens/second**. This includes concurrent outputs in each batch and should not be compared directly with single-request tokens/second. Its recorded session took about **2h 59m 05s through work completion**, before final archive packaging.

### Accuracy and uncertainty

The aim was substantial efficiency with comparable mathematical performance, not a higher benchmark score. The observed accuracy difference is small but remains part of the result.

For the original separate-adapter final evaluation, approximate paired, question-clustered 95% bootstrap intervals for accuracy change were:

- Against the standard baseline: **−2.78 to +0.22 percentage points**.
- Against the concise-prompt baseline: **−2.72 to −0.06 percentage points**.

These intervals belong to the original paired comparison, not the later merged repeat. Three sampled responses to one question are correlated; 1,800 responses are not 1,800 independent questions. Statistical equivalence or unchanged accuracy has not been established.

## Training

Two variants used the same deliberately small training budget:

- Ordinary cross-entropy fine-tuning on **20 selected positive traces**.
- The same fine-tuning plus a contextual unlikelihood penalty, using **20 annotated negative positions across 10 questions**.

Each variant received **five optimiser updates**, with gradient accumulation of eight, a learning rate of 0.00005, and rank-16 LoRA with alpha 32 and zero dropout. The penalty coefficient was 0.03.

The penalty discourages a particular next token in a particular annotated context. It is not a blanket ban on “wait”, “but” or “alternatively”: those words can also introduce useful correction. The project owner reviewed the annotations and approved proceeding within this limited scope.

After the initial pilot, six configurations were assessed on 200 development questions with three responses each:

| Configuration | Correct / 600 | Mean thinking tokens |
|---|---:|---:|
| Original — standard | 551 | 1,630 |
| Original — concise | 557 | 743 |
| Ordinary fine-tuning — standard | 554 | 744 |
| Ordinary fine-tuning — concise | 554 | 369 |
| Targeted-penalty fine-tuning — standard | 553 | 657 |
| Targeted-penalty fine-tuning — concise | 554 | 348 |

The targeted-penalty variant with concise prompting was selected before the final held-out evaluation. These results do not isolate the penalty as the sole cause of improvement: both ordinary fine-tuning and concise prompting were strong alternatives.

## Why inspect the reasoning?

A state-fair revenue problem provided a concrete example. Three attempts all reached the correct answer, **6,657**, but used **2,043, 2,246 and 7,029 thinking tokens**. The longest repeatedly questioned why food, ride and souvenir customer counts exceeded attendance, even though visitors could make purchases in multiple categories.

The useful target is unnecessary repetition and unsupported reinterpretation, while retaining checks that actually correct mistakes. Trace inspection informed the annotations; it was not a second mandatory mathematical score.

## Deployment investigation

The adapter initially ran separately, adding operations during generation. Merging incorporated its learned updates into the model weights; it did not add training.

A 30-question development diagnostic at batch size one found:

| Measurement | Separate adapter | Merged model |
|---|---:|---:|
| Mean generation time, fixed 256-token probe | 8.85 s | 4.81 s |
| Effective throughput on that probe | 28.9 tokens/s | 53.3 tokens/s |
| Mean complete-response generation time | 16.25 s | 8.67 s |
| Correct responses | 28/30 | 28/30 |

The fixed-length probe reduced the response-length confound and supported the adapter-overhead explanation. The subsequent full merged evaluation established the practical result at batch size four.

The exported BF16 model was saved, hash-checked, reloaded and used for all 1,800 responses. Its tensor fingerprint is:

`9aeef6382c69bb7997ce3061d0d039c7a8631a112e656f896c8b762728d2c9e8`

The complete weights remain in the local export; the compact evidence ZIP records their hashes. The model is named **LeanReasoning** and its complete checkpoint has been uploaded to [Hugging Face](https://huggingface.co/realDeclan/LeanReasoning). Distribution terms are specified in the custom [LeanReasoning Model Licence 1.0](../LICENSE-LEANREASONING.md), including the Microsoft exclusion and preservation of upstream rights.

## Supplementary diagnostics

A separate batch-size-one evaluation on 200 development questions measured mean response generation times of **36.2 s** for the original standard prompt, **19.5 s** for the original concise prompt and **15.6 s** for the trained concise model with its adapter separate. These are individual-response measurements, unlike the main workload timings.

A failure-retry diagnostic also repeated the 201 incorrect responses from the original trained final run, using fresh seeds and batch size one. **66 became correct; 135 remained incorrect.** This measures recovery on another attempt, not a replacement single-attempt accuracy score. The successful originals were not rerun in that diagnostic.

## Reproducibility

- Base model: Qwen3-1.7B; hardware: one NVIDIA RTX 3090.
- Final-answer scoring: pinned Hugging Face Math-Verify 0.9.0.
- Thinking enabled; temperature 0.6; top-p 0.95; top-k 20; maximum 8,192 generated tokens.
- Main evaluation batches: four responses.
- BF16 inference; the merged deployment used PyTorch scaled dot-product attention.
- Development, discovery/training and final question partitions were kept separate.
- Preserved schedules, prompts, seeds, raw outputs, scoring records and hashes are included in the evidence snapshots.

Standard answer instruction:

> Please reason step by step, and put your final answer within \boxed{}.

Additional concise instruction:

> Reason concisely. Avoid repeating calculations or checks that have already confirmed the result.

The merged run's replicate labels remain join labels; its actual batch RNG seeds differ from the first final evaluation. Reproduction should use the saved runner and schedules rather than infer seeds from those labels.

The latest evidence archive is `stage8_merged_2026-11-04_07-14.zip`. Its ZIP integrity and all 488 listed file hashes were checked. Earlier study snapshots and supporting diagnostics are preserved through GitHub Releases.

## Practical significance and scope

The merged workload occupied the GPU for approximately **9.03 fewer generation hours per 1,800 responses** than the standard baseline. Under the same hourly GPU rental rate, that corresponds to about **75% less generation-time spend**, excluding setup and other charges.

Shorter GPU workloads also offer a credible route to lower electricity use. This study did not record integrated power consumption, so it does not attach a measured kWh or percentage energy saving to that claim. Energy savings depend on average power as well as runtime.

At the observed mean lengths, 10,000 similar responses would avoid approximately **14.7 million thinking tokens** relative to the standard baseline. That is an illustrative extrapolation, not another measured dataset.

The conclusions apply to this small model, mathematical task distribution and inference stack. Larger models, broader tasks, reinforcement learning, on-policy distillation and extensive penalty tuning were outside the completed work.

## Conclusion

The project delivered a complete reasoning-compressed model and a reproducible evaluation pipeline. Targeted fine-tuning and concise prompting worked together, and deployment optimisation made the shorter reasoning substantially faster in practice. The final result is approximately four times the workload throughput with a modest observed accuracy trade-off.
