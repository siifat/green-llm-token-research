#!/usr/bin/env python3
import csv
from pathlib import Path
from statistics import mean, median


def pct_change(baseline, optimized):
    if baseline == 0:
        return 0.0
    return ((baseline - optimized) / baseline) * 100


def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    results_path = project_root / "data" / "processed" / "results.csv"

    if not results_path.exists():
        raise FileNotFoundError(f"Results file not found: {results_path}")

    with results_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != 100:
        raise RuntimeError(f"Expected 100 prompt pairs, found {len(rows)}.")

    for row in rows:
        for key in [
            "baseline_input_tokens",
            "optimized_input_tokens",
            "baseline_output_tokens",
            "optimized_output_tokens",
            "baseline_total_tokens",
            "optimized_total_tokens",
            "baseline_wall_time_s",
            "optimized_wall_time_s",
        ]:
            row[key] = float(row[key])

    b_in = sum(r["baseline_input_tokens"] for r in rows)
    o_in = sum(r["optimized_input_tokens"] for r in rows)

    b_out = sum(r["baseline_output_tokens"] for r in rows)
    o_out = sum(r["optimized_output_tokens"] for r in rows)

    b_total = sum(r["baseline_total_tokens"] for r in rows)
    o_total = sum(r["optimized_total_tokens"] for r in rows)

    b_time = sum(r["baseline_wall_time_s"] for r in rows)
    o_time = sum(r["optimized_wall_time_s"] for r in rows)

    fewer_input = sum(
        r["optimized_input_tokens"] < r["baseline_input_tokens"] for r in rows
    )
    fewer_output = sum(
        r["optimized_output_tokens"] < r["baseline_output_tokens"] for r in rows
    )
    fewer_total = sum(
        r["optimized_total_tokens"] < r["baseline_total_tokens"] for r in rows
    )
    faster = sum(
        r["optimized_wall_time_s"] < r["baseline_wall_time_s"] for r in rows
    )

    pair_reductions = [
        pct_change(r["baseline_total_tokens"], r["optimized_total_tokens"])
        for r in rows
    ]

    print("=== OVERALL EXPERIMENT SUMMARY ===")
    print(f"Prompt pairs: 100")
    print()
    print(f"Input tokens:  baseline={int(b_in):,}  optimized={int(o_in):,}  reduction={pct_change(b_in, o_in):.2f}%")
    print(f"Output tokens: baseline={int(b_out):,}  optimized={int(o_out):,}  reduction={pct_change(b_out, o_out):.2f}%")
    print(f"Total tokens:  baseline={int(b_total):,}  optimized={int(o_total):,}  reduction={pct_change(b_total, o_total):.2f}%")
    print()
    print(f"Wall time:     baseline={b_time:.2f}s  optimized={o_time:.2f}s  reduction={pct_change(b_time, o_time):.2f}%")
    print()
    print(f"Optimized used fewer input tokens in:  {fewer_input}/100 pairs")
    print(f"Optimized used fewer output tokens in: {fewer_output}/100 pairs")
    print(f"Optimized used fewer total tokens in:  {fewer_total}/100 pairs")
    print(f"Optimized was faster in:                {faster}/100 pairs")
    print()
    print(f"Mean pair-level total-token reduction:   {mean(pair_reductions):.2f}%")
    print(f"Median pair-level total-token reduction: {median(pair_reductions):.2f}%")
    print()
    print("PASS: Summary calculated from all 100 prompt pairs.")


if __name__ == "__main__":
    main()
