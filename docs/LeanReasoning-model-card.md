---
license: other
license_name: leanreasoning-model-license-1.0
license_link: https://huggingface.co/realDeclan/LeanReasoning/blob/main/LICENSE-LEANREASONING.md
base_model: Qwen/Qwen3-1.7B
base_model_relation: finetune
pipeline_tag: text-generation
library_name: transformers
tags:
- qwen3
- reasoning
- reasoning-compression
- merged-lora
- math
---
# LeanReasoning

**Shorter reasoning. Faster answers.**

LeanReasoning is a fine-tuned Qwen3-1.7B model designed to reduce unnecessary reasoning while retaining comparable mathematical accuracy.

With the evaluated concise prompt, it used **76% fewer thinking tokens** and **75% less batched generation time** than the original model with the standard prompt. Accuracy was **89% versus 90%**, rounded.

This is a **complete BF16 Transformers checkpoint** with the trained adapter merged into its weights. Load it directly: no separate adapter or PEFT loading step is required.

[Project and research archives](https://github.com/Rufus-Maxwell/Reasoning-Compression) · [Detailed report](https://github.com/Rufus-Maxwell/Reasoning-Compression/blob/main/docs/project-report-2026-11-04.md) · [Base model](https://huggingface.co/Qwen/Qwen3-1.7B)

## Results

Each configuration covers the same 600 final-evaluation questions, with three sampled responses per question: **1,800 responses per row**.

| Configuration | Correct | Accuracy | Mean thinking tokens | Batched generation time |
|---|---:|---:|---:|---:|
| Original Qwen3-1.7B — standard prompt | 1,622/1,800 | 90.11% | 1,940 | 12h 00m |
| Original Qwen3-1.7B — concise prompt | 1,624/1,800 | 90.22% | 1,036 | 7h 14m |
| **LeanReasoning — concise prompt, merged** | **1,599/1,800** | **88.83%** | **466** | **2h 58m** |

Against the original model with the **same concise prompt**, LeanReasoning used **55% fewer thinking tokens and 59% less generation time**. No responses in the merged-model evaluation reached the 8,192-token cap.

The main headline combines training, concise prompting and merged deployment. The exact observed accuracy difference was −1.28 percentage points against the standard baseline and −1.39 against the concise baseline; unchanged accuracy has not been established.

The model configuration was selected on development data before the first held-out evaluation. This merged-model measurement is a fresh-seed repeat on those same final questions, with no additional training. The original-model controls come from the first evaluation.

Timing covers generation in batches of four on a single RTX 3090. It excludes model loading, training, export, scoring and network overhead. It measures complete-workload runtime, **not individual-response latency**. Three responses to one question are correlated observations.

## Use the evaluated prompt

Append these two lines to the question:

```text
Please reason step by step, and put your final answer within \boxed{}.
Reason concisely. Avoid repeating calculations or checks that have already confirmed the result.
```

Use the included tokenizer's chat template with `enable_thinking=True`.

**The concise instruction is supplied by the caller.** It is not automatically inserted by the model or its tokenizer. The reported combined result depends on using it.

## Run with Transformers

The study used Transformers 4.56.2 and PyTorch 2.8.0+cu126. The example below targets a CUDA GPU with BF16 support and sufficient memory. It demonstrates single-response use, not the batched timing benchmark.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "realDeclan/LeanReasoning"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype=torch.bfloat16,
    attn_implementation="sdpa",
).to("cuda").eval()

question = "A shop sells 12 notebooks at £3 each. What is the total revenue?"
prompt = (
    question
    + "\nPlease reason step by step, and put your final answer within \\boxed{}."
    + "\nReason concisely. Avoid repeating calculations or checks that have already confirmed the result."
)
text = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=True,
)
inputs = tokenizer(
    text,
    add_special_tokens=False,
    return_tensors="pt",
).to(model.device)

with torch.inference_mode():
    outputs = model.generate(
        **inputs,
        do_sample=True,
        temperature=0.6,
        top_p=0.95,
        top_k=20,
        min_p=0.0,
        repetition_penalty=1.0,
        max_new_tokens=8192,
        use_cache=True,
        pad_token_id=tokenizer.eos_token_id,
    )

new_tokens = outputs[0, inputs["input_ids"].shape[-1]:]
print(tokenizer.decode(new_tokens, skip_special_tokens=False))
```

While this repository is private, authenticate with an account that has access before loading it. To use an existing local copy, set `model_id` to that folder's path.

The example prints the generated reasoning and answer. Sampling, batch size and software/hardware differences can change individual outputs; it is not an exact replay of the saved evaluation schedule.

## Training and export

LeanReasoning incorporates the project's `marker_003` LoRA adapter:

- Concise supervised fine-tuning on 20 selected positive traces.
- A contextual unlikelihood penalty of 0.03 at 20 annotated negative positions across 10 questions.
- Five optimiser updates; LoRA rank 16, alpha 32, dropout 0.
- BF16 merging into the original model, followed by saving, verification and reloading for evaluation.

The penalty discourages selected unwanted continuations in their annotated contexts. It is not a global ban on words such as “wait”, “but” or “alternatively”. The project owner reviewed the annotations.

This work was inspired by UkisAI's Swift research. It is an independent project, not an official Qwen or UkisAI release.

## Evaluation and scope

Final-answer correctness was scored using Hugging Face Math-Verify 0.9.0. Development, discovery/training and final question partitions were kept separate. The report contains the earlier separate-adapter results, development comparisons, uncertainty estimates and supporting diagnostics.

The measured improvement concerns mathematical reasoning under the stated prompts and generation settings. Broader improvements in coding, conversation, factual knowledge or other tasks have not been established.

Shorter runtime reduces GPU time required for this workload and can lower time-based hosting costs. Electricity consumption was not directly measured, so no numerical energy-saving claim is made.

## Files

The checkpoint contains two weight shards:

- `model-00001-of-00002.safetensors`
- `model-00002-of-00002.safetensors`

The accompanying index, model configuration, generation configuration, tokenizer and chat template are required parts of the export. Download the repository as a model folder.

## Licence and attribution

Base model: [Qwen/Qwen3-1.7B](https://huggingface.co/Qwen/Qwen3-1.7B).

The model is distributed under the [LeanReasoning Model Licence 1.0](LICENSE-LEANREASONING.md), a custom licence with Apache-2.0-based permissions for eligible recipients and an exclusion for Microsoft Corporation, its controlled/common-control entities, and parties acting on their behalf. This covers Copilot and all other uses, subject to the limited hosting exception described in the licence.

The unchanged upstream Apache 2.0 terms remain in [LICENSE](LICENSE). The custom restriction applies to the project's contributions and derivative distribution, not independently granted rights in Qwen's original model. This derivative modifies the original weights through fine-tuning and merging.
