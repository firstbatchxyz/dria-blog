---
categories:
- Applied AI
description: EvaluatePrediction evaluates the quality of predicted answers against
  questions and context, offering detailed feedback.
tags:
- evaluation
- AI
- predictions
- feedback
- data generation
---

# EvaluatePrediction

## Overview
EvaluatePrediction is a singleton class that evaluates the quality and correctness of a predicted answer in relation to a given question and context. It provides detailed evaluation feedback rather than just a boolean result.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| prediction | str | The predicted answer to be evaluated |
| question | str | The original question |
| context | str | The context against which to evaluate the prediction |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| question | str | The original question |
| prediction | str | The predicted answer being evaluated |
| evaluation | str | Detailed evaluation feedback |
| model | str | The AI model used for evaluation |

#### Usage

EvaluatePrediction instance can be used in data generation as follows:

```python
from dria.factory import EvaluatePrediction

my_dataset = DriaDataset(
    name="EvaluatePrediction",
    description="A dataset for prediction evaluation",
    schema=EvaluatePrediction.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
{
  "question": "Was Pope helpful in defense of Constantinople?",
  "prediction": "Based on the information provided, it appears that Pope Nicholas V's efforts were unlikely to be significantly helpful in defending Constantinople. The fact that many Western rulers were wary of increasing papal control and had financial constraints due to their own internal conflicts and wars suggests that they would not have been able or willing to contribute substantially to a defense effort",
  "evaluation": "[correct]",
  "model": "anthropic/claude-3-5-haiku-20241022:beta"
}
```