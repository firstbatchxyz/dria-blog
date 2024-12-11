---
categories:
- Applied AI
description: ValidatePrediction class for assessing the accuracy of AI predictions
  through contextual and semantic comparison.
tags:
- prediction validation
- semantic comparison
- AI model
- data generation
- contextual evaluation
---

# ValidatePrediction

## Overview
ValidatePrediction is a singleton class that validates whether a predicted answer matches a correct answer by performing contextual and semantic comparison. It provides a boolean validation result along with the original prediction and correct answer.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| prediction | str | The predicted answer to be evaluated |
| correct_answer | str | The correct answer to compare against |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| prediction | str | The original predicted answer |
| correct_answer | str | The original correct answer |
| validation | bool | Boolean result indicating if prediction matches correct answer |
| model | str | The AI model used for validation |

#### Usage

ValidatePrediction instance can be used in data generation as follows:

```python
from dria.factory import ValidatePrediction

my_dataset = DriaDataset(
    name="ValidatePrediction",
    description="A dataset for prediction validation",
    schema=ValidatePrediction.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
{
  "prediction": "Capital france is Berlin.",
  "correct_answer": "Capital of France is Paris",
  "validation": false,
  "model": "anthropic/claude-3-5-haiku-20241022:beta"
}
```