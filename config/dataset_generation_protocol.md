\# Dataset Generation Protocol



\## 1. Purpose



This protocol defines how the 500 experimental LLM tasks will be created.



The goal is to ensure that all team members create tasks using the same rules so that baseline and optimized prompts can be compared fairly.



\---



\# 2. Dataset Size



The final dataset will contain:



\- 500 underlying tasks

\- 5 task categories

\- 100 tasks per category



Each underlying task will contain:



1\. One baseline prompt

2\. One optimized prompt



Therefore:



500 tasks × 2 prompt variants = 1,000 primary LLM executions



\---



\# 3. Task Categories



The five allowed categories are:



1\. assignment\_writing

2\. exam\_preparation

3\. programming\_help

4\. concept\_learning

5\. research\_paper\_summarization



No additional categories should be created without team approval.



\---



\# 4. What Counts as One Task?



One task represents one specific student learning objective.



Example:



Underlying task:

Explain the four main principles of Object-Oriented Programming for exam preparation.



This is ONE task.



It then receives two prompt versions:



Baseline prompt:

An inefficient or unnecessarily token-consuming version.



Optimized prompt:

A more focused and token-efficient version.



Both versions must request essentially the same educational outcome.



\---



\# 5. Academic Eligibility Rule



A task can be included only when the scenario explicitly connects the LLM interaction to one of the following:



\- university coursework

\- course assignment

\- examination preparation

\- laboratory/coursework activity

\- university learning

\- formal academic research



Academic use must be determined from the stated purpose and context of the task.



It must NOT be determined only from the subject matter of the prompt.



Example:



"Explain photosynthesis."



This is ambiguous and should not be included without additional context.



Better:



"Explain photosynthesis for a first-year university biology exam."



This has an explicit university-learning context.



\---



\# 6. Baseline Prompt Rule



The baseline prompt represents a realistic but inefficient student prompt.



It may contain problems such as:



\- unnecessary verbosity

\- irrelevant context

\- repeated instructions

\- unnecessarily broad scope

\- requesting more detail than needed

\- asking the model to process unnecessary material

\- vague wording that causes unnecessarily large responses



The baseline prompt must still be realistic.



Do NOT intentionally create absurd or obviously artificial prompts solely to produce very high token usage.



Bad example:



"Write absolutely everything ever known about databases in 50,000 words."



This is unrealistic and should not be used.



\---



\# 7. Optimized Prompt Rule



The optimized prompt should reduce unnecessary token use while preserving the same underlying educational task.



Optimization may include:



\- removing redundant wording

\- removing irrelevant context

\- narrowing unnecessary scope

\- specifying the required output

\- targeting only relevant material

\- removing repeated instructions

\- replacing verbose wording with concise wording



The optimized prompt must NOT intentionally remove information that is necessary to complete the underlying task.



\---



\# 8. Same-Task Rule



This is one of the most important rules.



The baseline and optimized prompts must ask for the same underlying educational outcome.



Example:



Underlying task:

Explain the four principles of OOP for exam preparation.



Acceptable:



Baseline:

"Please explain Object-Oriented Programming in great detail for my university exam. I mainly need to understand the four major principles, so explain them clearly with useful examples and avoid assuming I already understand them."



Optimized:

"Explain the four OOP principles with brief examples for a university exam."



Both still request the four OOP principles.



Unacceptable:



Baseline:

"Explain OOP principles, history, advantages, disadvantages, applications, and future trends."



Optimized:

"List the four OOP principles."



These do not request the same amount of information.



\---



\# 9. Expected Content Rule



Each task must include an expected\_content field.



This defines the important content that a satisfactory response should contain.



Use semicolons to separate items.



Example:



Encapsulation; Inheritance; Polymorphism; Abstraction



Expected content will later help evaluators judge response completeness.



\---



\# 10. Subject Diversity



Tasks should come from multiple university subject areas.



Examples include:



\- Computer Science

\- Mathematics

\- Physics

\- Biology

\- Chemistry

\- Business

\- Economics

\- English

\- Engineering

\- Statistics

\- Social Science



The dataset should not consist almost entirely of Computer Science tasks.



Exact subject distribution will be decided separately.



\---



\# 11. External Context Files



Some tasks require external material.



Examples:



\- research paper summarization

\- programming code analysis

\- assignment material



When external material is required, store it in the appropriate contexts folder.



Examples:



contexts/papers/

contexts/code/

contexts/assignment\_materials/



The prompts.csv context\_file field should contain the relative path.



\---



\# 12. Prompt Identification



Each task receives one unique prompt\_id.



Format:



P0001

P0002

P0003

...

P0500



The same prompt\_id is used for both the baseline and optimized versions of that task.



\---



\# 13. Team Creation Rule



All four team members will contribute to prompt creation.



Each member will eventually create approximately 125 tasks.



Each member should create tasks across all five categories.



No member should create only one category.



\---



\# 14. Review Rule



Every task must be reviewed by a team member other than its creator.



The reviewer must check:



\- academic context is explicit

\- baseline prompt is realistic

\- optimized prompt is meaningfully more efficient

\- both prompts represent the same underlying task

\- expected\_content is sufficient

\- controlled vocabulary is used correctly

\- task is not a duplicate



A reviewed task may receive:



\- approved

\- rejected

\- returned for revision



\---



\# 15. Duplicate Rule



Two tasks should not test essentially the same scenario with only superficial wording changes.



Example:



Task 1:

Explain Newton's Second Law for a physics exam.



Task 2:

Explain F = ma for a physics exam.



These may be duplicates depending on their intended learning objective.



Reviewers should flag such cases.



\---



\# 16. Data Integrity Rule



Raw experimental results must never be altered to improve results.



Prompt pairs must not be modified after the main experiment begins unless the task is formally excluded and the reason is documented.



\---



\# 17. Pilot Requirement



Before creating all 500 tasks, the team will create a pilot dataset of 20 tasks.



Pilot structure:



\- 4 assignment\_writing

\- 4 exam\_preparation

\- 4 programming\_help

\- 4 concept\_learning

\- 4 research\_paper\_summarization



Each team member creates:



\- 1 task from each category



Therefore:



4 team members × 5 tasks = 20 pilot tasks



The pilot will be reviewed before full dataset generation begins.



\---



\# 18. Final Rule



Do not begin the 500-task dataset until the pilot has been reviewed and the dataset-generation rules have been confirmed.

