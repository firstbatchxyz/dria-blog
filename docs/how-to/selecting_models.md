---
categories:
- Applied AI
description: Learn how to select and assign models in the Dria Network for effective
  task execution with LLMs.
tags:
- Dria Network
- LLM Models
- Task Assignment
- Model Selection
- Artificial Intelligence
---

# Selecting Models

Dria Network is a network of LLMs.
When a task is published to the network, you can specify which models you want to assign your task to.

> See [models](models.md)

`Model` enum provides a list of models that you can use in your tasks.

```python
from dria import Model
```

`DatasetGenerator.generate()` has `models`param to assign models to your task.

Following task will be executed by `LLAMA3_1_8B_FP16` model. If the model is not available within network, SDK will poll the network until it finds an available `LLAMA3_1_8B_FP16` model.
```python
DatasetGenerator(dataset=dataset).generate(
    instructions=instructions, singletons=prompter, models=Model.LLAMA3_1_8B_FP16
)
```

**Model Availability?**

Dria Network consists of multiple nodes, each running one or more available models. When a task is published, nodes with the selected model execute the task asynchronously.

For example, if the network has 100 `Llama3.2-3B` models, publishing a task with the `Llama3.2-3B` model will be handled by one of those models. 
Publishing 100 tasks will distribute each to one of the 100 available models. 
However, if you publish a 101st task, task will wait in queue until a `Llama3.2-3B` model becomes available.

**Singe Task, Multiple Models**

Dria SDK enables you to publish a single task to multiple models. 
This is useful when you want to compare the results of different models on the same task.
Following example uses same instruction with different available open-source LLM and returns the results.


```python
instructions = [{"topic": "Decentralized synthetic data"}, {"topic": "Decentralized synthetic data"}]

DatasetGenerator(dataset=dataset).generate(
    instructions=instructions, singletons=prompter, models=[Model.LLAMA3_1_8B_FP16, Model.LLAMA_3_1_70B_OR]
)
```

You can also select providers as your models.
```python
# Providers
OLLAMA = "ollama"  # Open source models
OPENAI = "openai"  # OpenAI models
GEMINI = "gemini"  # Gemini models
OPENROUTER = "openrouter"  # OpenRouter models
CODER = "coder"  # Coder models
```