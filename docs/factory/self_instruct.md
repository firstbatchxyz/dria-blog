---
categories:
- Workflows
description: SelfInstruct automates user query generation for AI applications, enhancing
  testing and training efficiency.
tags:
- AI query generation
- automation
- data generation
- SelfInstruct
- training AI
---

# SelfInstruct

## Overview
SelfInstruct is a singleton template designed to generate user queries for AI applications based on specific criteria and context. It automates the process of creating relevant instructions or queries that can be used to test or train AI systems.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| num_instructions | conint(ge=1) | The number of user queries to generate |
| criteria_for_query_generation | str | The criteria for generating the queries |
| application_description | str | A description of the AI application |
| context | str | The context to which the queries should be applicable |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| instructions | List[str] | List of generated instructions |
| model | str | The AI model used for generation |

#### Usage

SelfInstruct instance can be used in data generation as follows:

```python
from dria.factory import SelfInstruct

my_dataset = DriaDataset(
    name="SelfInstruct",
    description="A dataset for self-instructed query generation",
    schema=SelfInstruct.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
{
   "instructions":[
      "Prioritize my upcoming deadlines, considering project dependencies. ",
      "Can you schedule a meeting with the marketing team for next week to discuss the Q3 campaign?",
      "Generate a comprehensive list of actionable steps required for completing the client proposal.",
      "What tasks are currently assigned to me that are due within the next 7 days?",
      "Remind me to follow up with John about the budget approval at 2 PM tomorrow."
   ],
   "model":"gemma2:9b-instruct-fp16"
}
```