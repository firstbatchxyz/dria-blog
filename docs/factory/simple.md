---
categories:
- Software Engineering
description: Generate text with the Simple Singleton task using instructions and select
  models like GEMINI for output.
tags:
- text generation
- Singleton pattern
- GEMINI model
- Python
- dria
---

# Simple

`Simple` is a `Singleton` task that generates text based on instruction.


#### Inputs
- prompt (`str`): The prompt to generate text from.

#### Outputs
- generation: (`str`): The generated text.
- model (`str`): The model used for code generation.

### Example

Generate text based on prompt. This examples uses `GEMMA2_9B_FP16` model.

```python
import os
import asyncio
from dria.factory import Simple
from dria.client import Dria
from dria.models import Task, Model

dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])


async def evaluate():
    simple = Simple()
    res = await dria.execute(
        Task(
            workflow=simple.workflow(prompt="Hey there!"),
            models=[Model.GEMINI_15_FLASH],
        )
    )
    return simple.parse_result(res)


def main():
    result = asyncio.run(evaluate())
    print(result)


if __name__ == "__main__":
    main()

```

Expected output:

```json
{
  "generation": "Hello! How can I assist you today?", 
  "model": "qwen2.5:7b-instruct-fp16"
}
```