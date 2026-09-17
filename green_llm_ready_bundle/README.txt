GREEN LLM TOKEN RESEARCH — READY INPUT BUNDLE

What changed
------------
The 25 previously missing inputs are now supplied.

- 5 non-paper tasks use researcher-created controlled inputs.
- 20 research-paper tasks use researcher-created synthetic paper texts.
- Synthetic papers are not real publications. They are controlled experimental stimuli.
- For research-paper tasks, the baseline receives the full synthetic paper text.
- The optimized prompt receives only the section(s) needed for the same task.
- All 100 prompt pairs are now marked experiment_ready = True.

Files
-----
green_llm_ready_100_prompts.csv
    Final machine-readable input dataset.

contexts/
    Context text files referenced by the CSV.

context_manifest.csv
    Maps each context-dependent prompt to its baseline and optimized context files.

synthetic_paper_catalog.csv
    Catalog of the synthetic paper stimuli.

Important methodology note
--------------------------
In the final report, disclose that the research-paper source documents were researcher-created
synthetic papers used to control content and make the experiment reproducible. Do not cite them
as real published studies.
