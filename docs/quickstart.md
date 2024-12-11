---
categories:
- Data Generation
description: Quick start guide to using Dria SDK for generating tweets with customizable
  prompts and dataset management.
tags:
- Dria SDK
- Dataset Generation
- Python
- Machine Learning
- Prompt Engineering
---

# Quick Start

> In order to follow this guide, you need to [install](installation.md) Dria SDK.


Using Dria is simple: 

- Create a dataset
- Attach a dataset generator
- Define your instructions (inputs)
- Define prompts
- Run!

```python
import asyncio
from dria import Prompt, DatasetGenerator, DriaDataset, Model
from pydantic import BaseModel, Field

# Define output schema
class Tweet(BaseModel):
    topic: str = Field(..., title="Topic")
    tweet: str = Field(..., title="tweet")

# Create dataset
dataset = DriaDataset(name="tweet_test", description="A dataset of tweets!", schema=Tweet)

# Create instructions
instructions = [{"topic": "BadBadNotGood"}, {"topic": "Decentralized synthetic data"}]

# Prompt to apply to your instructions
prompter = Prompt(prompt="Write a tweet about {{topic}}", schema=Tweet)

generator = DatasetGenerator(dataset=dataset)

asyncio.run(
    generator.generate(
        instructions=instructions, singletons=prompter, models=Model.GPT4O
    )
)

dataset.to_pandas()
#                          topic                                              tweet
# 0                 BadBadNotGood  🎶 Thrilled to have discovered #BadBadNotGood! ...
# 1  Decentralized Synthetic Data  Exploring the future of #AI with decentralized...
```

And that's it!
This script will run your instructions on models of your choice, execute them on a network of LLMs, and store them on a local database.


---

**Note**: Network capacity and data generation volumes are limited during the current phase of Dria.