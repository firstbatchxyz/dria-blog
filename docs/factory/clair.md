---
categories:
- Workflows
description: Clair is a SingletonTemplate task that corrects student solutions in
  programming, enhancing learning outcomes.
tags:
- student correction
- programming education
- machine learning
- educational technology
- code review
---

# Clair

`Clair` is a `SingletonTemplate` task that takes a student solution and reasoning, and corrects the student solution.

#### Inputs
- task (`str`): The task description or problem statement.
- student_solution (`str`): The student's original solution to be corrected.

#### Outputs
- reasoning (`str`): The teacher's reasoning for the corrections.
- corrected_student_solution (`str`): The improved version of the student's solution.
- task (`str`): The original task description (echoed from input).
- student_solution (`str`): The original student solution (echoed from input).
- model (`str`): The model used for code generation.


```python
from dria.factory import Clair

my_dataset = DriaDataset(
    name="clair",
    description="A dataset for clair",
    schema=Clair.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

#### Expected output

```json
{
   "reasoning":"##  Understanding Factorials\n\nFactorial (represented by the symbol \"!\") means multiplying a number by all the whole numbers less than it down to 1. For example, 5! = 5 * 4 * 3 * 2 * 1 = 120.\n\n****: The provided code has a small syntax error.  In Python, colons (`:`) are used to indicate the start of a block of code, not as part of the return statement itself.\n\n\n **",
   "corrected_student_solution":"**:\n\n```python\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1) \n```\n\n\n\nLet me break down how this corrected code works:\n\n1. **Base Case:** The `if n == 0:` statement checks if the input number is 0. If it is, the function returns 1 because 0! is defined as 1.\n\n2. **Recursive Step:**  If `n` is not 0, the `else` block executes. It calculates the factorial by multiplying `n` with the factorial of `",
   "task":"Write a function to calculate the factorial of a number.",
   "student_solution":"def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
   "model":"gemma2:9b-instruct-fp16"
}
```

#### References
- [Distilabel CLAIR](https://distilabel.argilla.io/latest/components-gallery/tasks/clair/)
-[Anchored Preference Optimization and Contrastive Revisions: Addressing Underspecification in Alignment
](https://arxiv.org/abs/2408.06266v1)
- [CLAIR_and_APO](https://github.com/ContextualAI/CLAIR_and_APO)