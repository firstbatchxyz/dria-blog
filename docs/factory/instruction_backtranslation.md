---
categories:
- Applied AI
description: Learn about Instruction Backtranslation, a Singleton task for evaluating
  text outputs against reference instructions with scoring.
tags:
- Instruction Backtranslation
- AI Evaluation
- Text Output Analysis
- Parallel Execution
- Model Scoring
---

# InstructionBacktranslation

## Overview
InstructionBacktranslation is a singleton class that evaluates instruction-generation pairs. It processes an original instruction and its generated text, providing a score and reasoning for the evaluation.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| instruction | str | The original instruction to be evaluated |
| generation | str | The generated text to be evaluated against the instruction |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| reasoning | str | Detailed explanation for the evaluation score |
| score | str | Evaluation score for the instruction-generation pair |
| instruction | str | Original instruction (echoed from input) |
| generation | str | Generated text (echoed from input) |
| model | str | The AI model used for evaluation |

#### Usage

InstructionBacktranslation instance can be used in data generation as follows:

```python
from dria.factory import InstructionBacktranslation

my_dataset = DriaDataset(
    name="instruction_backtranslation",
    description="A dataset for instruction-generation pair evaluation",
    schema=InstructionBacktranslation.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
[
  {
    "reasoning": "The response is concise, accurate, and directly answers the user's question.  There's no unnecessary information or fluff. It's a perfect example of a simple, effective AI assistant response.",
    "score": "5",
    "instruction": "What is 3 times 20?",
    "generation": "It's 60.",
    "model": "gemini-1.5-flash"
  },
  {
    "reasoning": "The candidate answer is incorrect, as it fails to provide the correct answer to the math question \"What is 3 times 20?\" The correct response should be \"The answer is 60.\" Since the candidate answer gives an incorrect result and does not demonstrate any helpfulness or relevance to the user's request, it is a poor response overall.",
    "score": "1",
    "instruction": "What is 3 times 20?",
    "generation": "It's 59.",
    "model": "gpt-4o-mini"
  }
]
```

## References

- [Distilabel InstructionBacktranslation](https://distilabel.argilla.io/latest/components-gallery/tasks/instructionbacktranslation/)
- [Self-Alignment with Instruction Backtranslation](https://arxiv.org/pdf/2308.06259)