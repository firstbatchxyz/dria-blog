---
categories:
- Data Generation
description: Explore the DatasetGenerator tool by Dria for efficient dataset creation
  and transformation using prompt and singleton workflows.
tags:
- dataset generation
- data transformation
- Dria
- AI workflows
- synthetic data
---

# Dataset Generator

`DatasetGenerator` is a powerful tool for generating and transforming datasets using Dria, supporting both prompt-based and singleton-based data generation workflows.

## Core Features

- Parallel execution capabilities
- Automatic schema validation
- Multiple model support
- Search capabilities
- Sequential workflow processing

## Basic Usage

DatasetGenerator requires a DriaDataset to operate. 

### Using Prompts

Prompt-based generation is a simple way to generate data using a single prompt. Dria will apply the prompt to each instruction.
Prompts are defined using the `Prompt` class. 

```python
import asyncio
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field


# Define output schema
class Tweet(BaseModel):
    topic: str = Field(..., title="Topic")
    tweet: str = Field(..., title="tweet")


# Create dataset
dataset = DriaDataset(
    name="tweet_test", description="A dataset of tweets!", schema=Tweet
)
```

After dataset is created, you can define instructions and prompts to apply to the instructions.
Prompts accept variables with double curly braces `{{variable}}`.

```python
instructions = [{"topic": "BadBadNotGood"}, {"topic": "Decentralized synthetic data"}]

prompter = Prompt(prompt="Write a tweet about {{topic}}", schema=Tweet)
generator = DatasetGenerator(dataset=dataset)

asyncio.run(
    generator.generate(
        instructions=instructions, singletons=prompter, models=Model.GPT4O
    )
)

print(dataset.to_pandas())
```

### Using Singletons

Dria provides a factory for [pre-built](../factory/simple.md) singletons. Singletons are custom classes that define a specific workflow for generating data. 

```python
from dria import DriaDataset, DatasetGenerator, Model
from dria.factory import GenerateSubtopics

my_dataset = DriaDataset(
    name="subtopics",
    description="A dataset for subtopics",
    schema=GenerateSubtopics.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

## Model Configuration

### Single Model
```python
models = Model.GPT4O
```

### Multiple Models
```python
models = [Model.GPT4O, Model.GEMINI_15_FLASH]
```

### Model Pipeline
```python
models = [
    [Model.GPT4O],           # For first singleton
    [Model.GEMINI_15_FLASH], # For second singleton
    [Model.LLAMA3_1_8B_FP16] # For third singleton
]
```