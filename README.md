\# Green LLM Token Research



\## Project Title



Reducing Token Waste in Student LLM Use for University Learning Tasks:

Implications for Sustainable AI Computing



\## Project Purpose



This project investigates whether unnecessary token consumption in university-related LLM interactions can be reduced through prompt optimization while preserving response quality and educational usefulness.



The study compares baseline prompts with optimized prompts for the same underlying academic task.



\## Dataset Design



Target:



\- 500 underlying university-learning tasks

\- 5 task categories

\- 100 tasks per category

\- 2 prompt variants per task:

&#x20; - baseline

&#x20; - optimized

\- 1 primary execution per variant



Expected primary LLM executions:



500 × 2 = 1,000 runs



\## Task Categories



1\. assignment\_writing

2\. exam\_preparation

3\. programming\_help

4\. concept\_learning

5\. research\_paper\_summarization



\## Academic Scope



A task is included only when its experimental context explicitly connects the LLM interaction to a university course, assessment, examination, coursework, laboratory activity, or formal research activity.



Academic classification is based on the stated purpose and context of the interaction rather than on prompt subject matter alone.



Ambiguous general-purpose tasks are excluded.



\## Data Files



\### data/prompts/prompts.csv



Master dataset containing the 500 experimental tasks.



Each task contains:



\- academic context

\- underlying task

\- baseline prompt

\- optimized prompt

\- optimization strategy

\- expected content

\- metadata



\### data/raw/runs.jsonl



Raw LLM execution data.



Each line represents one model execution.



Raw experiment data must never be manually modified or overwritten.



\### data/evaluation/quality\_scores.csv



Human evaluation scores for generated responses.



Evaluation dimensions:



\- accuracy

\- completeness

\- educational\_usefulness



All dimensions use integer scores from 1 to 5.



\### data/processed/results.csv



Processed paired results comparing baseline and optimized executions.



This file will be generated automatically by analysis scripts.



\## Project Structure



green-llm-token-research/

│

├── data/

│   ├── prompts/

│   │   └── prompts.csv

│   ├── raw/

│   │   └── runs.jsonl

│   ├── evaluation/

│   │   └── quality\_scores.csv

│   └── processed/

│       └── results.csv

│

├── contexts/

│   ├── papers/

│   ├── code/

│   └── assignment\_materials/

│

├── scripts/

│   └── validate\_prompts.py

│

├── notebooks/

│

├── figures/

│

├── logs/

│

├── config/

│   ├── controlled\_vocabulary.json

│   ├── data\_dictionary.csv

│   ├── run\_data\_dictionary.csv

│   ├── quality\_data\_dictionary.csv

│   ├── results\_data\_dictionary.csv

│   ├── experiment\_config.json

│   └── quality\_rubric.md

│

└── README.md



\## Experimental Principles



1\. Baseline and optimized prompts must represent the same underlying task.



2\. Prompt optimization must not intentionally change the required educational outcome.



3\. Raw experimental outputs must never be overwritten.



4\. Failed executions and retries must remain recorded.



5\. Token counts and latency are directly measured experimental variables.



6\. Quality is evaluated separately using the predefined human evaluation rubric.



7\. Environmental and computational implications are estimated separately from directly measured variables.



8\. Dataset validation must pass before experiments are executed.



\## Dataset Validation



Run:



python scripts/validate\_prompts.py



The main experiment must not begin if validation reports blocking errors.

