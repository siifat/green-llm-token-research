#!/usr/bin/env python3
import argparse
import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError

MODEL = "gemma3:4b"
OLLAMA_URL = "http://localhost:11434/api/generate"
TEMPERATURE = 0
SEED = 42
MAX_RETRIES = 4


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def call_ollama(prompt: str):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "seed": SEED,
        },
        "keep_alive": "30m",
    }

    data = json.dumps(payload).encode("utf-8")

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        req = request.Request(
            OLLAMA_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        start = time.perf_counter()

        try:
            with request.urlopen(req, timeout=1800) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            wall_time_s = time.perf_counter() - start
            return result, wall_time_s

        except HTTPError as e:
            try:
                server_message = e.read().decode("utf-8", errors="replace")
            except Exception:
                server_message = ""

            last_error = RuntimeError(
                f"HTTP {e.code}: {e.reason}"
                + (f" | Ollama message: {server_message}" if server_message else "")
            )

        except (URLError, TimeoutError, ConnectionError) as e:
            last_error = e

        if attempt < MAX_RETRIES:
            wait_s = min(5 * (2 ** (attempt - 1)), 20)
            print(
                f"\n    Ollama error on attempt {attempt}/{MAX_RETRIES}. "
                f"Retrying in {wait_s}s..."
            )
            time.sleep(wait_s)

    raise RuntimeError(
        f"Ollama failed after {MAX_RETRIES} attempts: {last_error}"
    )


def build_full_prompt(prompt_text: str, context_path: Path | None):
    if context_path is None:
        return prompt_text

    context_text = context_path.read_text(encoding="utf-8")
    return (
        f"{prompt_text}\n\n"
        "SOURCE MATERIAL:\n"
        "----------------\n"
        f"{context_text}"
    )


def load_completed_runs(output_path: Path):
    completed = set()

    if not output_path.exists():
        return completed

    with output_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(
                    f"Warning: ignoring malformed line {line_number} "
                    f"in {output_path.name}"
                )
                continue

            prompt_id = record.get("prompt_id")
            variant = record.get("variant")

            if (
                prompt_id
                and variant in {"baseline", "optimized"}
                and record.get("response_text") is not None
                and record.get("input_tokens") is not None
                and record.get("output_tokens") is not None
            ):
                completed.add((prompt_id, variant))

    return completed


def append_jsonl(path: Path, record: dict):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run only the first N tasks."
    )
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    bundle_dir = project_root / "green_llm_ready_bundle"
    csv_path = bundle_dir / "green_llm_ready_100_prompts.csv"

    output_path = project_root / "data" / "raw" / "runs.jsonl"
    error_path = project_root / "logs" / "experiment_errors.jsonl"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    error_path.parent.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Could not find dataset:\n{csv_path}\n"
            "Make sure green_llm_ready_bundle is inside the project folder."
        )

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    if args.limit is not None:
        rows = rows[:args.limit]

    expected_pairs = {
        (row["prompt_id"], variant)
        for row in rows
        for variant in ("baseline", "optimized")
    }

    completed = load_completed_runs(output_path)
    completed_in_scope = completed & expected_pairs
    remaining = expected_pairs - completed_in_scope

    print(f"Model: {MODEL}")
    print(f"Tasks in scope: {len(rows)}")
    print(f"Expected runs: {len(expected_pairs)}")
    print(f"Already completed: {len(completed_in_scope)}")
    print(f"Remaining: {len(remaining)}")
    print(f"Output: {output_path}")

    if not remaining:
        print("\nNothing to do. All runs in scope are already complete.")
        return

    # Warm-up request: excluded from experiment data.
    print("\nWarming up the model...")
    try:
        call_ollama("Reply with exactly: READY")
    except Exception as e:
        raise RuntimeError(
            "Ollama could not complete the warm-up request. "
            "Make sure Ollama is running, then try again."
        ) from e
    print("Warm-up complete.\n")

    failed_this_pass = []

    for task_index, row in enumerate(rows, start=1):
        prompt_id = row["prompt_id"]

        # Keep the same balanced order rule as the original script.
        variants = (
            ["baseline", "optimized"]
            if task_index % 2 == 1
            else ["optimized", "baseline"]
        )

        for run_order, variant in enumerate(variants, start=1):
            run_key = (prompt_id, variant)

            if run_key in completed:
                print(
                    f"[{task_index}/{len(rows)}] "
                    f"{prompt_id} - {variant} ... SKIPPED (already complete)"
                )
                continue

            prompt_col = f"{variant}_prompt"
            context_col = f"{variant}_context_file"

            prompt_text = row[prompt_col]
            context_rel = (row.get(context_col) or "").strip()
            context_path = (bundle_dir / context_rel) if context_rel else None

            if context_path is not None and not context_path.exists():
                error_record = {
                    "timestamp_utc": utc_now(),
                    "prompt_id": prompt_id,
                    "variant": variant,
                    "error_type": "missing_context_file",
                    "error": str(context_path),
                }
                append_jsonl(error_path, error_record)
                failed_this_pass.append(run_key)
                print(
                    f"[{task_index}/{len(rows)}] "
                    f"{prompt_id} - {variant} ... FAILED (missing context file)"
                )
                continue

            full_prompt = build_full_prompt(prompt_text, context_path)

            print(
                f"[{task_index}/{len(rows)}] "
                f"{prompt_id} - {variant} ...",
                end=" ",
                flush=True
            )

            try:
                result, wall_time_s = call_ollama(full_prompt)
            except Exception as e:
                print("FAILED after retries")

                error_record = {
                    "timestamp_utc": utc_now(),
                    "prompt_id": prompt_id,
                    "variant": variant,
                    "error_type": type(e).__name__,
                    "error": str(e),
                }
                append_jsonl(error_path, error_record)
                failed_this_pass.append(run_key)

                # Do not kill the whole experiment.
                # A later rerun will try only unfinished runs.
                continue

            input_tokens = result.get("prompt_eval_count")
            output_tokens = result.get("eval_count")

            total_tokens = (
                input_tokens + output_tokens
                if isinstance(input_tokens, int)
                and isinstance(output_tokens, int)
                else None
            )

            record = {
                "timestamp_utc": utc_now(),
                "prompt_id": prompt_id,
                "source_pair_id": row["source_pair_id"],
                "category": row["category"],
                "task": row["task"],
                "variant": variant,
                "run_order_within_pair": run_order,
                "model": MODEL,
                "temperature": TEMPERATURE,
                "seed": SEED,
                "prompt_text": prompt_text,
                "context_file": context_rel,
                "full_prompt": full_prompt,
                "response_text": result.get("response", ""),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "wall_time_s": round(wall_time_s, 6),
                "ollama_total_duration_s": round(
                    result.get("total_duration", 0) / 1_000_000_000, 6
                ),
                "load_duration_s": round(
                    result.get("load_duration", 0) / 1_000_000_000, 6
                ),
                "prompt_eval_duration_s": round(
                    result.get("prompt_eval_duration", 0) / 1_000_000_000, 6
                ),
                "eval_duration_s": round(
                    result.get("eval_duration", 0) / 1_000_000_000, 6
                ),
                "done_reason": result.get("done_reason"),
            }

            append_jsonl(output_path, record)
            completed.add(run_key)

            print(
                f"done | in={input_tokens} out={output_tokens} "
                f"total={total_tokens} time={wall_time_s:.2f}s"
            )

    final_completed = load_completed_runs(output_path) & expected_pairs
    missing = sorted(expected_pairs - final_completed)

    print("\nRun pass finished.")
    print(f"Completed: {len(final_completed)}/{len(expected_pairs)}")
    print(f"Still missing: {len(missing)}")

    if missing:
        print("\nMissing runs:")
        for prompt_id, variant in missing:
            print(f"  - {prompt_id} {variant}")

        print(
            "\nRun the SAME command again later. "
            "The script will skip completed runs and retry only the missing ones."
        )
    else:
        print("\nAll experimental runs completed successfully.")


if __name__ == "__main__":
    main()
