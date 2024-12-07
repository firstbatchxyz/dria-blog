---
categories:
- Workflows
description: Learn how to use the Prompt class in Dria for generating structured outputs
  with schema validation using Pydantic models.
tags:
- Prompt
- Pydantic
- Data Generation
- Dria
- Schema Validation
---

# Prompt

The `Prompt` class is a simple singleton template that allows you to create prompts with schema validation using Pydantic models. It provides a straightforward way to generate structured outputs from language models.

## Basic Usage

### 1. Import Required Dependencies
```python
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field
```

### 2. Define Output Schema
Create a Pydantic model that defines the structure of your expected output:

```python
class OutputSchema(BaseModel):
    field1: str = Field(..., title="Field1")
    field2: str = Field(..., title="Field2")
```

### 3. Create Dataset
Initialize a DriaDataset with your schema:

```python
dataset = DriaDataset(
    name="my_dataset",
    description="Dataset description",
    schema=OutputSchema
)
```

### 4. Initialize Prompt
Create a Prompt instance with your prompt text and schema. Add variables in the prompt text using double curly braces `{{}}`:

```python
prompter = Prompt(prompt="Do something with {{field1}}", schema=OutputSchema)
```

### 5. Generate Data
Use DatasetGenerator to execute the prompt:

```python
generator = DatasetGenerator(dataset=dataset)
instructions = [{"field1": "value1"}, {"field2": "value2"}]

asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=Model.LLAMA_3_1_8B_OR
    )
)
```

## Complete Example

Here's a complete example that generates tweets about different topics:

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
    name="tweet_test",
    description="A dataset of tweets!",
    schema=Tweet
)

# Define instructions
instructions = [
    {"topic": "BadBadNotGood"},
    {"topic": "Decentralized synthetic data"}
]

# Create prompt
prompter = Prompt(prompt="Write a tweet about {{topic}}", schema=Tweet)

# Initialize generator
generator = DatasetGenerator(dataset=dataset)

# Generate data
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=prompter,
        models=Model.GPT4O
    )
)

# View results
dataset.to_pandas()
```

`Prompt` is useful for straightforward tasks. For more complex tasks, consider creating a custom singleton using the `SingletonTemplate` class.