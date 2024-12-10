---
categories:
- Preference Data
description: Rank instructions by complexity using the ScoreComplexity singleton task,
  providing scores and model references for guidance.
tags:
- Complexity Scoring
- Instructions Ranking
- Machine Learning
- Task Automation
- Data Analysis
---

# ScoreComplexity

## Overview
ScoreComplexity is a singleton that evaluates and assigns complexity scores to a list of instructions. It analyzes each instruction and provides a numerical score representing its complexity level.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| instructions | List[str] | List of instructions to be scored for complexity |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| instruction | str | The instruction being scored |
| score | int | Numerical complexity score assigned to the instruction |
| model | str | The AI model used for scoring |

#### Usage

ScoreComplexity instance can be used in data generation as follows:

```python
from dria.factory import ScoreComplexity

my_dataset = DriaDataset(
    name="score_complexity",
    description="A dataset for instruction complexity scoring",
    schema=ScoreComplexity.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

#### Expected output

```json
[
   {
      "instruction":"Boil water in a kettle",
      "score":3,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Write a research paper on quantum physics",
      "score":5,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Tie your shoelaces",
      "score":4,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Develop a machine learning algorithm",
      "score":5,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Make a sandwich",
      "score":2,
      "model":"llama3.1:8b-instruct-fp16"
   }
]
```

#### References
- [ComplexityScorer Distilabel](https://distilabel.argilla.io/latest/components-gallery/tasks/complexityscorer)
- [What Makes Good Data for Alignment? A Comprehensive Study of Automatic Data Selection in Instruction Tuning](https://arxiv.org/abs/2312.15685)