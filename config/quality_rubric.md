# Quality Evaluation Rubric

Each LLM response is evaluated independently on three dimensions:

1. Accuracy
2. Completeness
3. Educational Usefulness

Each dimension receives an integer score from 1 to 5.

---

## 1. Accuracy

### Score 5 — Excellent
The response is factually correct and contains no meaningful errors.

### Score 4 — Good
The response is mostly correct but contains a minor error or imprecision that does not significantly affect the answer.

### Score 3 — Acceptable
The response contains some factual or conceptual errors, but the main answer remains substantially correct.

### Score 2 — Poor
The response contains major errors or misleading information that significantly reduces correctness.

### Score 1 — Very Poor
The response is largely incorrect, fundamentally misleading, or fails to answer the task correctly.

---

## 2. Completeness

Completeness must be judged relative to the underlying task and the expected_content field in prompts.csv.

### Score 5 — Excellent
All or nearly all important required points are addressed sufficiently.

### Score 4 — Good
Most important points are covered, with only minor omissions.

### Score 3 — Acceptable
The core task is addressed, but several relevant or expected points are missing.

### Score 2 — Poor
Large parts of the required content are missing.

### Score 1 — Very Poor
The response fails to cover most of the required content or does not meaningfully complete the task.

---

## 3. Educational Usefulness

Educational usefulness measures how useful the response would be to a university student performing the stated task.

### Score 5 — Excellent
Clear, relevant, appropriately structured, and highly useful for the stated academic task.

### Score 4 — Good
Useful and understandable, with minor issues such as unnecessary detail, weak organization, or limited explanation.

### Score 3 — Acceptable
Provides some educational value but may be unclear, poorly organized, too verbose, too brief, or insufficiently tailored to the task.

### Score 2 — Poor
Provides limited educational value and would require substantial improvement before being useful to the student.

### Score 1 — Very Poor
Not useful for the stated academic task, seriously unclear, irrelevant, or inappropriate for the requested purpose.

---

# Evaluation Rules

1. Evaluate the generated response, not the quality of the prompt.

2. Use only integer scores:
   1, 2, 3, 4, or 5.

3. Judge completeness against:
   - the underlying_task,
   - task_context,
   - expected_content.

4. Do not reward a response simply for being longer.

5. Do not penalize a response simply for being shorter.

6. A concise response can receive a score of 5 if it fully satisfies the task.

7. Excessive verbosity may reduce educational_usefulness if it makes the answer less focused or harder to use.

8. Baseline and optimized responses must be judged using the same standards.

9. Evaluators should score each response independently before discussing disagreements.

10. Evaluators should not change scores merely to make baseline and optimized responses appear similar.

11. If the evaluator lacks enough subject knowledge to judge accuracy reliably, the response should be flagged for review rather than guessed.

12. Optional comments should briefly explain unusual scores, major errors, omissions, or other important observations.
