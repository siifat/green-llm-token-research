import csv
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROMPTS_FILE = PROJECT_ROOT / "data" / "prompts" / "prompts.csv"
VOCAB_FILE = PROJECT_ROOT / "config" / "controlled_vocabulary.json"

REQUIRED_FIELDS = [
    "prompt_id",
    "category",
    "subject_area",
    "difficulty",
    "course_context",
    "academic_context_type",
    "underlying_task",
    "task_context",
    "baseline_prompt",
    "optimized_prompt",
    "optimization_strategy",
    "expected_content",
    "created_by",
    "status",
]


def load_vocabulary():
    with open(VOCAB_FILE, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def load_prompts():
    with open(PROMPTS_FILE, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def validate():
    vocabulary = load_vocabulary()
    rows = load_prompts()

    errors = []
    warnings = []

    seen_ids = set()

    for row_number, row in enumerate(rows, start=2):
        prompt_id = row.get("prompt_id", "").strip()

        # Check required fields
        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                errors.append(
                    f"Row {row_number}: required field '{field}' is empty."
                )

        # Validate prompt ID
        if prompt_id and not re.fullmatch(r"P\d{4}", prompt_id):
            errors.append(
                f"Row {row_number}: invalid prompt_id '{prompt_id}'. "
                f"Expected format such as P0001."
            )

        # Duplicate prompt ID
        if prompt_id in seen_ids:
            errors.append(
                f"Row {row_number}: duplicate prompt_id '{prompt_id}'."
            )
        elif prompt_id:
            seen_ids.add(prompt_id)

        # Controlled vocabulary checks
        for field in [
            "category",
	    "difficulty",
            "academic_context_type",
            "optimization_strategy",
            "status",
        ]:
            value = row.get(field, "").strip()

            if value and value not in vocabulary[field]:
                errors.append(
                    f"Row {row_number}: invalid {field} '{value}'. "
                    f"Allowed values: {vocabulary[field]}"
                )

        # Baseline and optimized prompts should not be identical
        baseline = row.get("baseline_prompt", "").strip()
        optimized = row.get("optimized_prompt", "").strip()

        if baseline and optimized and baseline == optimized:
            errors.append(
                f"Row {row_number}: baseline_prompt and optimized_prompt "
                f"are identical."
            )

        # Check context file if specified
        context_file = row.get("context_file", "").strip()

        if context_file:
            context_path = PROJECT_ROOT / Path(context_file)

            if not context_path.exists():
                errors.append(
                    f"Row {row_number}: referenced context file "
                    f"'{context_file}' does not exist."
                )

        # Warning for very short expected_content
        expected_content = row.get("expected_content", "").strip()

        if expected_content and len(expected_content) < 10:
            warnings.append(
                f"Row {row_number}: expected_content may be too vague."
            )

    print("=" * 60)
    print("PROMPT DATASET VALIDATION")
    print("=" * 60)

    print(f"Rows checked: {len(rows)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print()

    if errors:
        print("ERRORS")
        print("-" * 60)

        for error in errors:
            print(f"[ERROR] {error}")

        print()

    if warnings:
        print("WARNINGS")
        print("-" * 60)

        for warning in warnings:
            print(f"[WARNING] {warning}")

        print()

    if not errors:
        print("VALIDATION PASSED")
        print("No blocking errors were found.")
    else:
        print("VALIDATION FAILED")
        print("Fix all errors before running experiments.")


if __name__ == "__main__":
    validate()