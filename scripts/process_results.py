#!/usr/bin/env python3
import csv
import json
from pathlib import Path


def pct_reduction(baseline, optimized):
    if baseline in (None, 0) or optimized is None:
        return None
    return round(((baseline - optimized) / baseline) * 100, 2)


def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    input_path = project_root / "data" / "raw" / "runs.jsonl"
    output_path = project_root / "data" / "processed" / "results.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Raw results not found: {input_path}")

    records = []
    with input_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise RuntimeError(
                    f"Invalid JSON on line {line_number} of {input_path}"
                ) from e

    if len(records) != 200:
        raise RuntimeError(f"Expected 200 raw runs, found {len(records)}.")

    by_prompt = {}
    for r in records:
        pid = r["prompt_id"]
        variant = r["variant"]

        if variant not in {"baseline", "optimized"}:
            raise RuntimeError(f"Unexpected variant for {pid}: {variant}")

        by_prompt.setdefault(pid, {})
        if variant in by_prompt[pid]:
            raise RuntimeError(f"Duplicate run found: {pid} {variant}")

        by_prompt[pid][variant] = r

    if len(by_prompt) != 100:
        raise RuntimeError(f"Expected 100 prompt pairs, found {len(by_prompt)}.")

    rows = []

    for pid in sorted(by_prompt):
        pair = by_prompt[pid]

        if set(pair) != {"baseline", "optimized"}:
            raise RuntimeError(f"Incomplete pair for {pid}: {sorted(pair)}")

        b = pair["baseline"]
        o = pair["optimized"]

        if b["category"] != o["category"]:
            raise RuntimeError(f"Category mismatch for {pid}")

        if b["source_pair_id"] != o["source_pair_id"]:
            raise RuntimeError(f"Source pair mismatch for {pid}")

        row = {
            "prompt_id": pid,
            "source_pair_id": b["source_pair_id"],
            "category": b["category"],
            "task": b["task"],
            "model": b["model"],
            "temperature": b["temperature"],
            "seed": b["seed"],

            "baseline_input_tokens": b["input_tokens"],
            "optimized_input_tokens": o["input_tokens"],
            "input_token_reduction": b["input_tokens"] - o["input_tokens"],
            "input_token_reduction_pct": pct_reduction(
                b["input_tokens"], o["input_tokens"]
            ),

            "baseline_output_tokens": b["output_tokens"],
            "optimized_output_tokens": o["output_tokens"],
            "output_token_reduction": b["output_tokens"] - o["output_tokens"],
            "output_token_reduction_pct": pct_reduction(
                b["output_tokens"], o["output_tokens"]
            ),

            "baseline_total_tokens": b["total_tokens"],
            "optimized_total_tokens": o["total_tokens"],
            "total_token_reduction": b["total_tokens"] - o["total_tokens"],
            "total_token_reduction_pct": pct_reduction(
                b["total_tokens"], o["total_tokens"]
            ),

            "baseline_wall_time_s": b["wall_time_s"],
            "optimized_wall_time_s": o["wall_time_s"],
            "wall_time_reduction_s": round(
                b["wall_time_s"] - o["wall_time_s"], 6
            ),
            "wall_time_reduction_pct": pct_reduction(
                b["wall_time_s"], o["wall_time_s"]
            ),

            "baseline_ollama_total_duration_s": b.get("ollama_total_duration_s"),
            "optimized_ollama_total_duration_s": o.get("ollama_total_duration_s"),
            "ollama_duration_reduction_pct": pct_reduction(
                b.get("ollama_total_duration_s"),
                o.get("ollama_total_duration_s"),
            ),

            "optimized_used_fewer_input_tokens": (
                o["input_tokens"] < b["input_tokens"]
            ),
            "optimized_used_fewer_output_tokens": (
                o["output_tokens"] < b["output_tokens"]
            ),
            "optimized_used_fewer_total_tokens": (
                o["total_tokens"] < b["total_tokens"]
            ),
            "optimized_was_faster": (
                o["wall_time_s"] < b["wall_time_s"]
            ),
        }

        rows.append(row)

    fieldnames = list(rows[0].keys())

    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"PASS: Processed {len(rows)} complete prompt pairs.")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
