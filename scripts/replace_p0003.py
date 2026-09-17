#!/usr/bin/env python3
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

NEW_SOURCE_PAIR = "1.26"
NEW_TASK = "Write the discussion of a net present value appraisal for a finance assignment."

NEW_BASELINE = (
    "For my university Corporate Finance assignment I had to appraise a proposed "
    "investment using net present value and I have got a positive NPV figure. Now I "
    "need to write the discussion. Could you please write about 250 words explaining "
    "what the positive NPV means for the decision, what assumptions the calculation "
    "depends on, and what sensitivity analysis would add? Please write it formally "
    "for a finance report."
)

NEW_OPTIMIZED = (
    "For a university Corporate Finance assignment, write a 250-word discussion "
    "of a positive net present value result. Ensure the output covers:\n"
    "1. What the positive NPV implies for the investment decision.\n"
    "2. The key assumptions the figure depends on.\n"
    "3. The value of sensitivity analysis."
)

REPLACEMENT_NOTE = (
    "Replaced original P0003 after Gemma 3 4B repeatedly aborted the baseline "
    "with Ollama token-repeat-limit errors. Reserve Assignment Writing pair 1.26 "
    "was selected. Model settings were not changed."
)


def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    dataset = project_root / "green_llm_ready_bundle" / "green_llm_ready_100_prompts.csv"
    runs = project_root / "data" / "raw" / "runs.jsonl"
    logs = project_root / "logs"
    logs.mkdir(parents=True, exist_ok=True)

    if not dataset.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset}")

    # Read dataset.
    with dataset.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    matches = [r for r in rows if r.get("prompt_id") == "P0003"]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one P0003 row, found {len(matches)}.")

    current = matches[0]

    # Safety guard: do not delete a valid replacement run if this script is run twice.
    if current.get("source_pair_id") == NEW_SOURCE_PAIR:
        print("P0003 is already replaced with reserve pair 1.26.")
        print("No files were changed.")
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = logs / f"p0003_replacement_backup_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=False)

    shutil.copy2(dataset, backup_dir / dataset.name)
    if runs.exists():
        shutil.copy2(runs, backup_dir / runs.name)

    old_snapshot = dict(current)

    # Replace only the P0003 dataset row.
    current.update({
        "source_pair_id": NEW_SOURCE_PAIR,
        "category": "assignment_writing",
        "task": NEW_TASK,
        "baseline_prompt": NEW_BASELINE,
        "optimized_prompt": NEW_OPTIMIZED,
        "modified": "True",
        "cleaning_notes": REPLACEMENT_NOTE,
        "context_required": "False",
        "context_requirement": "",
        "experiment_ready": "True",
        "baseline_context_file": "",
        "optimized_context_file": "",
        "context_source": "none",
        "context_status": "not_required",
    })

    temp_dataset = dataset.with_suffix(".csv.tmp")
    with temp_dataset.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temp_dataset.replace(dataset)

    # Remove any old P0003 run records so BOTH replacement variants run again.
    removed = 0
    if runs.exists():
        kept_lines = []
        with runs.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    kept_lines.append(line)
                    continue
                try:
                    rec = json.loads(stripped)
                except json.JSONDecodeError:
                    kept_lines.append(line)
                    continue

                if rec.get("prompt_id") == "P0003":
                    removed += 1
                else:
                    kept_lines.append(line)

        temp_runs = runs.with_suffix(".jsonl.tmp")
        with temp_runs.open("w", encoding="utf-8") as f:
            f.writelines(kept_lines)
        temp_runs.replace(runs)

    log_entry = {
        "timestamp_local": datetime.now().isoformat(),
        "prompt_id": "P0003",
        "old_source_pair_id": old_snapshot.get("source_pair_id"),
        "old_task": old_snapshot.get("task"),
        "new_source_pair_id": NEW_SOURCE_PAIR,
        "new_task": NEW_TASK,
        "reason": REPLACEMENT_NOTE,
        "old_run_records_removed": removed,
        "backup_dir": str(backup_dir),
    }

    replacement_log = logs / "p0003_replacement.json"
    replacement_log.write_text(
        json.dumps(log_entry, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("P0003 replacement completed.")
    print(f"New source pair: {NEW_SOURCE_PAIR}")
    print(f"Old P0003 run records removed: {removed}")
    print(f"Backup saved to: {backup_dir}")
    print("")
    print("Next command:")
    print(r"python .\scripts\run_experiment.py")


if __name__ == "__main__":
    main()
