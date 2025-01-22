---
categories:
- Data Generation
description: Simple is a singleton template for text generation, enabling straightforward
  workflows with customizable prompts and models.
tags:
- text generation
- singleton template
- data generation
- prompts
- workflow
---

# Simple

## Overview
Simple is a singleton template implementation for basic text generation. It takes a prompt as input and generates text using a specified model, providing a straightforward workflow for text generation tasks.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| prompt | str | Input prompt for generation |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| prompt | str | The prompt used to generate text |
| generation | str | Generated text |
| model | str | Model used for generation |

#### Usage

Simple instance can be used in data generation as follows:

```python
from dria.factory import Simple

my_dataset = DriaDataset(
    name="Simple",
    description="A dataset for simple text generation",
    schema=Simple.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output:

```json
{
  "prompt": "Hey there!",
  "generation": "Hello! How can I assist you today?", 
  "model": "qwen2.5:7b-instruct-fp16"
}
```