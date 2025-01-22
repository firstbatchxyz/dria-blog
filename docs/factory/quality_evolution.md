---
categories:
- Data Generation
description: EvolveQuality enhances text responses using AI with methods like helpfulness,
  relevance, and creativity for better data generation outcomes.
tags:
- AI
- Data Generation
- Response Enhancement
- Quality Improvement
- Machine Learning
---

# EvolveQuality

## Overview
EvolveQuality is a singleton template that evolves or improves text responses based on specific quality dimensions. It takes an original response and enhances it according to one of several methods: helpfulness, relevance, depth, creativity, or detail level.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| prompt | str | The original prompt or context |
| response | str | The response text to be evolved |
| method | Literal | Evolution method to apply ("HELPFULNESS", "RELEVANCE", "DEEPENING", "CREATIVITY", "DETAILS") |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| response | str | The original response text |
| evolved_response | str | The evolved/rewritten response |
| method | str | Method used for evolution |
| model | str | The AI model used for generation |

#### Usage

EvolveQuality instance can be used in data generation as follows:

```python
from dria.factory import EvolveQuality

my_dataset = DriaDataset(
    name="EvolveQuality",
    description="A dataset for response quality evolution",
    schema=EvolveQuality.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

The singleton supports five evolution methods:
- HELPFULNESS: Makes the response more helpful to the user
- RELEVANCE: Improves relevance to the given prompt
- DEEPENING: Increases the depth of the response
- CREATIVITY: Enhances creative aspects
- DETAILS: Adds more detailed information

### Expected output

```json
{
   "response":"Photosynthesis is the process by which plants make their own food using sunlight.",
   "evolved_response":"Photosynthesis is a complex biochemical process through which plants, algae, and some bacteria convert light energy into chemical energy. This process occurs in the chloroplasts of plant cells and involves two main stages: the light-dependent reactions and the light-independent reactions (Calvin cycle). During the light-dependent reactions, chlorophyll and other pigments in the thylakoid membranes absorb sunlight, which drives the splitting of water molecules into oxygen, protons, and electrons. This creates a proton gradient that powers the production of ATP. The light-independent reactions use the energy from ATP and NADPH (produced in the light-dependent reactions) to fix carbon dioxide from the air into glucose through a series of enzymatic reactions. This glucose serves as the primary energy source for the plant and can be used to synthesize other organic compounds necessary for growth and development. Photosynthesis is crucial for life on Earth, as it produces oxygen as a byproduct and forms the base of most food chains in ecosystems.",
   "method":"DEEPENING",
   "model":"gemma2:9b-instruct-fp16"
}
```

#### References
- [EvolInstruct Distilabel](https://distilabel.argilla.io/latest/components-gallery/tasks/evolquality/)
- [What Makes Good Data for Alignment? A Comprehensive Study of Automatic Data Selection in Instruction Tuning](https://arxiv.org/abs/2312.15685)