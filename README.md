# Green LLM Token Research

## Project Title

**Reducing Token Waste in Student LLM Use for University Learning Tasks: Implications for Sustainable AI Computing**

## Project Purpose

This project investigates whether unnecessary token consumption in university-related LLM interactions can be reduced through prompt optimization while preserving response quality and educational usefulness.

For each task, we compare two prompt versions:

- **Baseline:** a normal student-style prompt.
- **Optimized:** a shorter, clearer, and more structured version of the same request.

The goal is not simply to make prompts shorter. The goal is to reduce **total token use and computational effort** without changing the required educational outcome.

---

## Final Experimental Design

- **100 underlying university-learning tasks**
- **5 task categories**
- **20 tasks per category**
- **2 prompt variants per task:** baseline and optimized
- **1 primary execution per variant**
- **200 executions per model**
- **4 final LLM models**

```text
100 tasks × 2 variants = 200 runs per model
200 runs × 4 models = 800 primary runs
```

## Task Categories

1. `assignment_writing`
2. `exam_preparation`
3. `programming_help`
4. `concept_learning`
5. `research_paper_summarization`

## Academic Scope

A task is included only when its context clearly connects the LLM interaction to a university course, assignment, examination, coursework, laboratory activity, university learning, or formal research.

Academic classification is based on the **purpose and context** of the interaction, not only on the topic of the prompt. Ambiguous general-purpose tasks are excluded.

---

# Methodology

## 1. Dataset Preparation

A larger pool of candidate prompt pairs was first prepared across the five categories. For the final experiment, **20 prompt pairs from each category** were selected, giving **100 tasks**.

The final dataset is:

```text
green_llm_ready_bundle/green_llm_ready_100_prompts.csv
```

An Excel copy is also included for manual review.

Each task contains the academic task, baseline prompt, optimized prompt, category, and any required supporting context.

## 2. Baseline and Optimized Prompts

The baseline and optimized prompts must request the **same educational outcome**.

The optimized prompt removes unnecessary wording and improves structure, but it is not allowed to reduce the required work simply to produce a shorter answer.

All 100 pairs were manually reviewed before execution. Small fairness corrections were made where necessary so both versions represented the same task.

## 3. Supporting Context

Some tasks require source material such as assignment information, code, reading material, or paper content. These materials are stored in the project context files and are automatically appended to the relevant prompt.

For the research-paper summarization category, we use **researcher-created synthetic papers** as controlled experimental stimuli. These are not real published papers. They were created so the same controlled source material could be used consistently across model runs.

## 4. P0003 Replacement

During the original Gemma experiment, the first version of `P0003` repeatedly failed with:

```text
prediction aborted, token repeat limit reached
```

Because the failure continued under the fixed experimental settings, we did not change the model settings for that one prompt. Instead, the original P0003 was replaced with reserve Assignment Writing pair `1.26`, a Corporate Finance task about interpreting a positive NPV result.

Both baseline and optimized variants were replaced together. The same replacement dataset is used for all later model experiments.

## 5. Models

The final study uses four different model families:

| Model | Ollama identifier | Environment |
|---|---|---|
| Gemma 3 4B | `gemma3:4b` | Local PC, AMD Ryzen 7 7700 CPU |
| Llama 3.2 3B Instruct | `llama3.2:3b-instruct-q4_K_M` | Google Colab, NVIDIA T4 GPU |
| Qwen2.5 3B Instruct | `qwen2.5:3b-instruct` | Google Colab, NVIDIA T4 GPU |
| Ministral 3 3B Instruct | `ministral-3:3b-instruct-2512-q4_K_M` | Google Colab, NVIDIA T4 GPU |

Ollama is used as the model-serving interface.

### Abandoned Phi Pilot

Phi-3.5 Mini 3.8B was briefly tested as a possible fourth model. During pilot testing, its P0001 baseline repeatedly entered the same token-repeat failure pattern. The full Phi experiment was therefore not run, and Ministral was used instead.

## 6. Controlled Generation Settings

The main settings are kept fixed:

```text
Temperature: 0
Seed: 42
Runs per prompt variant: 1
```

The same final dataset and supporting context files are used for every model.

## 7. Run Order

Each task contains one baseline run and one optimized run.

To reduce order bias:

- odd-numbered tasks run baseline first,
- even-numbered tasks run optimized first.

A warm-up request is sent before measured runs begin. The warm-up is not included in the experimental results.

## 8. Experiment Runner

The Python runner:

- loads the final CSV dataset,
- adds the required context,
- sends requests to the Ollama API,
- records the complete response,
- records token counts and timing,
- saves every completed run immediately,
- retries temporary failures,
- and safely resumes after interruption.

The runner is **resume-safe**: completed `(prompt_id, variant)` combinations are skipped when the same experiment is restarted.

## 9. Data Recorded

For each successful execution, the raw JSONL record includes:

- timestamp,
- prompt ID,
- source pair ID,
- category,
- task description,
- prompt variant,
- run order,
- model,
- temperature,
- seed,
- prompt text,
- context file,
- complete prompt sent to the model,
- complete generated response,
- input tokens,
- output tokens,
- total tokens,
- wall-clock response time,
- Ollama timing information,
- and completion reason.

Raw model outputs are not manually edited.

## 10. Efficiency Measurements

For each matched baseline/optimized pair, we compare:

- input-token reduction,
- output-token reduction,
- total-token reduction,
- response-time reduction,
- whether the optimized prompt used fewer total tokens,
- and whether the optimized prompt completed faster.

```text
total tokens = input tokens + output tokens
```

Total token use is important because a shorter input prompt can sometimes cause a longer output. Therefore, input-token reduction alone is not treated as sufficient evidence of improved efficiency.

## 11. Human Quality Evaluation

Token reduction alone is not enough. Generated responses are also scored by humans on:

1. **Accuracy**
2. **Completeness**
3. **Educational Usefulness**

Each dimension uses an integer score from **1 to 5**.

The same standard is applied to baseline and optimized responses. A shorter response can still receive a high score if it is accurate, complete, and useful.

## 12. Multi-Model Comparison

The same 100-task protocol is repeated across all four final models.

The purpose is not to rank the models. The main question is whether prompt optimization shows a similar efficiency effect across different LLM families.

Gemma ran on local CPU hardware while the other final models run on Google Colab T4 GPUs. Therefore, raw execution time is **not** used to directly rank model speed across different hardware environments.

Latency is mainly interpreted as the baseline-to-optimized change **within the same model and environment**.

## 13. Sustainability Interpretation

The experiment directly measures:

- input tokens,
- output tokens,
- total tokens,
- and response latency.

It does **not** directly measure electricity use, carbon emissions, or water consumption.

Environmental implications are therefore discussed separately using relative computational-efficiency reasoning and supporting literature.

---

# Current Experiment Status

## Gemma 3 4B

Status: **Completed and validated**

```text
100 baseline runs
100 optimized runs
200 total runs
```

Initial overall summary:

```text
Input-token reduction: 54.82%
Output-token reduction: 15.13%
Total-token reduction: 23.67%
Wall-time reduction: 17.19%
Optimized used fewer total tokens in 83/100 pairs
Optimized was faster in 80/100 pairs
```

## Ministral 3 3B Instruct

Status: **Completed and validated**

```text
100 baseline runs
100 optimized runs
200 total runs
```

Initial overall summary:

```text
Input-token reduction: 17.45%
Output-token reduction: 16.88%
Total-token reduction: 17.16%
Wall-time reduction: 17.32%
Optimized used fewer total tokens in 70/100 pairs
Optimized was faster in 63/100 pairs
```

## Llama 3.2 3B Instruct

Status: **Separate Colab experiment using the same 100-pair protocol**

## Qwen2.5 3B Instruct

Status: **Separate Colab experiment using the same 100-pair protocol**

Final cross-model analysis will be completed after all four raw result files are collected.

---

# Main Data Files

## Final Prompt Dataset

```text
green_llm_ready_bundle/green_llm_ready_100_prompts.csv
```

Also available as:

```text
green_llm_ready_bundle/green_llm_ready_100_prompts.xlsx
```

## Context Manifest

```text
green_llm_ready_bundle/context_manifest.csv
```

## Synthetic Paper Catalog

```text
green_llm_ready_bundle/synthetic_paper_catalog.csv
```

## Raw Results

```text
data/raw/runs.jsonl
data/raw/runs_llama32_3b_colab.jsonl
data/raw/runs_qwen25_3b_colab.jsonl
data/raw/runs_ministral3_3b_colab.jsonl
```

`runs.jsonl` contains the original Gemma experiment.

## Human Quality Scores

```text
data/evaluation/quality_scores.csv
```

## Processed Pair Results

```text
data/processed/results.csv
```

---

# Project Structure

```text
green-llm-token-research/
├── green_llm_ready_bundle/
│   ├── green_llm_ready_100_prompts.csv
│   ├── green_llm_ready_100_prompts.xlsx
│   ├── context_manifest.csv
│   ├── synthetic_paper_catalog.csv
│   ├── README.txt
│   └── contexts/
│
├── data/
│   ├── raw/
│   │   ├── runs.jsonl
│   │   ├── runs_llama32_3b_colab.jsonl
│   │   ├── runs_qwen25_3b_colab.jsonl
│   │   └── runs_ministral3_3b_colab.jsonl
│   ├── evaluation/
│   │   └── quality_scores.csv
│   └── processed/
│       └── results.csv
│
├── scripts/
│   ├── run_experiment.py
│   ├── run_experiment_llama32_colab.py
│   ├── run_experiment_qwen25_colab.py
│   ├── run_experiment_ministral3_colab.py
│   ├── process_results.py
│   ├── summarize_results.py
│   └── validate_prompts.py
│
├── config/
├── logs/
├── notebooks/
├── figures/
└── README.md
```

---

# Experimental Principles

1. Baseline and optimized prompts must represent the same underlying task.
2. Optimization must not intentionally reduce the required educational outcome.
3. The same final 100-task dataset is used across models.
4. Raw experimental outputs must not be manually overwritten.
5. Failed executions and important retries should remain documented.
6. Input tokens, output tokens, total tokens, and latency are directly measured variables.
7. Shorter input prompts are not automatically assumed to be more efficient; total tokens are also evaluated.
8. Response quality is evaluated separately using the predefined human rubric.
9. Environmental implications are estimated separately from directly measured variables.
10. Cross-hardware latency values are not used for direct model-speed ranking.

---

# Validation and Reproducibility

Before a full experiment, verify that:

- the final 100-pair dataset is present,
- P0003 uses replacement source pair `1.26`,
- all required context files are present,
- the correct model is loaded,
- temperature is `0`,
- seed is `42`,
- and the output filename is unique to that model.

After a full experiment, verify:

```text
200 total records
100 baseline records
100 optimized records
200 unique (prompt_id, variant) combinations
one consistent model/temperature/seed configuration
non-empty generated responses
positive token counts
positive response times
normal completion reasons
```

---

# Analysis Workflow

1. Validate raw model outputs.
2. Convert raw JSONL into paired baseline/optimized results.
3. Calculate token and latency reductions.
4. Compare results by task category.
5. Perform human quality evaluation.
6. Compare efficiency results with quality scores.
7. Compare whether the optimization pattern is consistent across models.
8. Interpret computational and sustainability implications.
9. Document limitations and final conclusions.

---

# Important Limitations

Token reduction is used as an indicator of reduced computational workload, not as a direct measurement of environmental impact.

The research-paper tasks use controlled synthetic papers rather than real publications. This improves experimental control but reduces ecological validity for that category.

The model experiments are also not all executed on identical hardware, so raw latency cannot be used as a direct cross-model speed comparison.

---

# Project Goal

The final goal is to determine whether clearer and more efficient prompting can reduce unnecessary LLM token consumption in university learning tasks while maintaining useful educational responses, and whether this effect appears consistently across multiple LLM families.
