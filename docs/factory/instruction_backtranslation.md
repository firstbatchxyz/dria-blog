---
categories:
- Applied AI
description: Learn about Instruction Backtranslation for scoring text generation based
  on given instructions, using parallel execution across models.
tags:
- Instruction Backtranslation
- AI Evaluation
- Text Generation
- Score Generation
- Parallel Execution
---

# Instruction Backtranslation

`InstructionBackTranslation` is a `Singleton` task that generates a score (1-5) and reason for a given instruction and generation 

### Inputs
instruction (`str`): The reference instruction to evaluate the text output.
generation (`str`): The text output to evaluate for the given instruction.

### Outputs
score (`str`): The score for the generation based on the given instruction.
reason (`str`): The reason for the provided score.
model_name (`str`): The model name used to score the generation.

### Example

We'll use `ParallelSingletonExecutor` to run multiple `InstructionBackTranslation` task in parallel across multiple models.

```python
from dria.client import Dria
from dria.factory import InstructionBacktranslation
from dria.models import Model
from dria.batches import ParallelSingletonExecutor
import asyncio
import json

async def batch():
    dria_client = Dria()
    singleton = InstructionBacktranslation()
    executor = ParallelSingletonExecutor(dria_client, singleton)
    executor.set_models([Model.GPT4O])
    executor.load_instructions(
        [
            {
                "instruction": "What is 3 times 20?",
                "generation": "It's 60.",
            },
            {
                "instruction": "What is 3 times 20?",
                "generation": "It's 59.",
            },
        ]
    )
    return await executor.run()


def main():
    results = asyncio.run(batch())
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

```

#### Expected output

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