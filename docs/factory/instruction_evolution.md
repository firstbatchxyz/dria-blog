---
categories:
- Workflows
description: EvolveInstruct mutates prompts using diverse strategies while preserving
  core intent, enhancing data generation and complexity.
tags:
- prompt evolution
- data generation
- mutation strategies
- AI prompts
- EvolveInstruct
---

# EvolveInstruct

## Overview
EvolveInstruct is a singleton template designed to mutate or evolve prompts in various ways. It provides different mutation strategies to transform an original prompt into a new version while maintaining its core intent. The mutations can add constraints, deepen complexity, make prompts more concrete, increase reasoning requirements, or switch topics while maintaining similar difficulty levels.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| prompt | str | The original prompt to be mutated |
| mutation_type | MutationType | The type of mutation to apply (one of: FRESH_START, ADD_CONSTRAINTS, DEEPEN, CONCRETIZE, INCREASE_REASONING, SWITCH_TOPIC) |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| mutated_prompt | str | The transformed version of the original prompt |
| original_prompt | str | The input prompt (echoed from input) |
| model | str | The AI model used for generation |

#### Usage

EvolveInstruct instance can be used in data generation as follows:

```python
from dria.factory import EvolveInstruct

my_dataset = DriaDataset(
    name="evolve_instruct",
    description="A dataset for prompt evolution",
    schema=EvolveInstruct.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

The mutation types available are:
- FRESH_START: Creates a new question using specified keywords
- ADD_CONSTRAINTS: Adds additional requirements to the original prompt
- DEEPEN: Increases the complexity and scope of the prompt
- CONCRETIZE: Makes the prompt more specific and concrete
- INCREASE_REASONING: Transforms the prompt to require multi-step reasoning
- SWITCH_TOPIC: Changes the topic while maintaining similar difficulty and domain


### Expected output

```json
{
   "mutated_prompt":"**Discuss the intricate process of photosynthesis, delving into its two main stages (light-dependent and light-independent reactions).  Explain how sunlight is captured, water is split, and carbon dioxide is fixed to produce glucose, the primary energy source for plants. Describe the role of chlorophyll and other pigments in absorbing light energy, and outline the significance of photosynthesis for life on Earth, including its impact on oxygen production and the global carbon cycle.** \n\n\nThis new prompt:\n\n* **Increases depth:** It asks for a more detailed explanation, including the two stages of photosynthesis and their specific mechanisms.\n* **Increases breadth:**  It expands the scope to include the roles of chlorophyll, pigments, and the broader ecological significance of photosynthesis.",
   "prompt":"Explain the concept of photosynthesis.",
   "model":"gemma2:9b-instruct-fp16"
}
```

#### References
- [EvolInstruct Distilabel](https://distilabel.argilla.io/latest/components-gallery/tasks/evolinstruct/#input-output-columns)
- [WizardLM: Empowering Large Language Models to Follow Complex Instructions](https://arxiv.org/abs/2304.12244)
- [GitHub: h2oai/h2o-wizardlm](https://github.com/h2oai/h2o-wizardlm)