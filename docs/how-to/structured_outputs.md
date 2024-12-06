---
categories:
- Workflows
description: Learn how to implement structured outputs with Dria SDK for generating
  consistent and reliable responses in Python.
tags:
- Structured Outputs
- Dria SDK
- Python
- Book Review Generation
- Workflow
---

# Structured Outputs

> Structured Outputs supported after version dria==0.0.65

Structured outputs best explained in OpenAI's [blog post](https://platform.openai.com/docs/guides/structured-outputs):

> Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema, so you don't need to worry about the model omitting a required key, or hallucinating an invalid enum value. 


Dria Network supports structured outputs for all providers including `OpenAI`, `Gemini` and `Ollama`.
However, structured outputs are only supported by models that are capable of [function](functions.md) calling. 

Enabling structured outputs is simple. You just need to provide a schema to the `WorkflowBuilder` instance, rest will be handled by Dria SDK.

Lets walkthrough a simple example where we generate a book review using structured outputs. See full code [here](#full-code).

First we define a schema for the book review:

```python
from pydantic import BaseModel, Field

class BookReview(BaseModel):
    """Book review specification."""
    title: str = Field(..., description="Book title")
    rating: int = Field(..., description="Rating from 1-5 stars")
    genre: str = Field(..., description="Book genre")
    review_text: str = Field(..., description="Short review text")
    recommended: bool = Field(..., description="Whether the book is recommended")
```

Now we'll create a `SingletonTemplate` instance:

```python
class BookReviewSingleton(SingletonTemplate):
    """Workflow generator."""
    def workflow(self, **kwargs) -> Workflow:
        pass
    
    def parse_result(self, result: List[TaskResult]):
        pass
```

`workflow` is used to define task and `parse_result` is used to parse the results. 

```python
from dria.factory.workflows.template import SingletonTemplate
from dria.models import Task, Model, TaskResult
from dria.factory.utilities import parse_json
from dria_workflows import Workflow, WorkflowBuilder, Operator, Edge, Write
from typing import List

class BookReviewSingleton(SingletonTemplate):
    """Workflow generator."""

    def workflow(self) -> Workflow:
        builder = WorkflowBuilder()
        builder.set_max_tokens(2000)
        builder.set_max_time(120)
        builder.set_max_steps(20)

        builder.generative_step(
            prompt="Create a simple book review",
            schema=BookReview,
            operator=Operator.GENERATION,
            outputs=[Write.new("response")]
        )
        
        # Define the flow of execution
        builder.flow([Edge(source="0", target="_end")])
        
        # Set the return value, read 'response' key from memory as return value
        builder.set_return_value("response")
        return builder.build()

    def parse_result(self, result: List[TaskResult]):
        """Parse results."""
        return [{"generation": parse_json(r.result), "model": r.model} for r in result]
```
    
That's it! We have defined a structured output for book review generation.

We'll run it using the following code:

```python
async def execute_workflow(dria: Dria, **kwargs):
    tasks = Task(workflow=Generator().workflow(**kwargs), models=[Model.GPT4O_MINI])
    res = await dria.execute(tasks)
    return Generator().parse_result(res)


if __name__ == "__main__":
    dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])
    print(asyncio.run(execute_workflow(dria, num_samples=1)))
```

Parsed result:

```json
[
    {
        "generation": {
            "genre": "Fiction",
            "rating": 4,
            "recommended": true,
            "review_text": "A captivating story with compelling characters and exquisite prose. The plot twists kept me on the edge of my seat!",
            "title": "The Whispering Woods"
        },
        "model": "gpt-4o-mini"
    }
]
```

Voila! We have successfully generated a book review using structured outputs.

---

##### *Full code*:

See the full code to execute a book review generation task using structured outputs:

```python
import asyncio
from typing import List

from dria.client import Dria
from dria.factory.workflows.template import SingletonTemplate
from dria.models import Task, Model, TaskResult
from dria.factory.utilities import parse_json
from dria_workflows import Workflow, WorkflowBuilder, Operator, Edge, Write
from pydantic import BaseModel, Field
import json
import os


class BookReview(BaseModel):
    """Book review specification."""
    title: str = Field(..., description="Book title")
    rating: int = Field(..., description="Rating from 1-5 stars")
    genre: str = Field(..., description="Book genre")
    review_text: str = Field(..., description="Short review text")
    recommended: bool = Field(..., description="Whether the book is recommended")


class BookReviewSingleton(SingletonTemplate):
    """Workflow generator."""

    def workflow(self) -> Workflow:
        builder = WorkflowBuilder()
        builder.set_max_tokens(2000)
        builder.set_max_time(120)
        builder.set_max_steps(20)

        builder.generative_step(
            prompt="Create a simple book review",
            schema=BookReview,
            operator=Operator.GENERATION,
            outputs=[Write.new("response")]
        )

        builder.flow([Edge(source="0", target="_end")])
        builder.set_return_value("response")
        return builder.build()

    def parse_result(self, result: List[TaskResult]):
        """Parse results."""
        return [{"generation": parse_json(r.result), "model": r.model} for r in result]


async def execute_workflow(dria: Dria):
    task = Task(workflow=BookReviewSingleton().workflow(), models=[Model.GPT4O_MINI])
    res = await dria.execute(task)
    return BookReviewSingleton().parse_result(res)


if __name__ == "__main__":
    dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])
    print(json.dumps(asyncio.run(execute_workflow(dria)), indent=4))

```