---
categories:
- Workflows
description: EvolveComplexity transforms instructions into more complex versions while
  preserving their meaning, ideal for data generation and instruction variations.
tags:
- instruction evolution
- data generation
- AI language model
- complexity transformation
- variations
---

# EvolveComplexity

## Overview
EvolveComplexity is a singleton that takes an instruction and evolves it into a more complex version while maintaining the core meaning and intent. This is useful for creating variations of instructions with different complexity levels.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| instruction | str | The original instruction to be evolved |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| evolved_instruction | str | The evolved version of the instruction with increased complexity |
| instruction | str | Original instruction (echoed from input) |
| model | str | The AI model used for generation |

#### Usage

EvolveComplexity instance can be used in data generation as follows:

```python
from dria.factory import EvolveComplexity

my_dataset = DriaDataset(
    name="evolve_complexity",
    description="A dataset for instruction evolution",
    schema=EvolveComplexity.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
{
   "evolved_instruction":"Write a short story about a cat who, unbeknownst to its human family, communicates with other cats in a secret language that revolves around solving mysteries within the neighborhood. The cat must navigate between two worlds: the simple life of domesticity and the complex web of feline intrigue, all while trying not to reveal their dual life to their human companions.",
   "instruction":"Write a short story about a cat.",
   "model":"qwen2.5:32b-instruct-fp16"
}
```

#### References
- [EvolComplexity Distilabel](https://distilabel.argilla.io/latest/components-gallery/tasks/evolcomplexity/)
- [WizardLM: Empowering Large Language Models to Follow Complex Instructions](https://arxiv.org/abs/2304.12244)
- [GitHub: h2oai/h2o-wizardlm](https://github.com/h2oai/h2o-wizardlm)