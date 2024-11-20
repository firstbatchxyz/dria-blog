---
categories:
- Workflows
description: A Python example demonstrating asynchronous execution of multiple AI
  models using the Dria library.
tags:
- Python
- Dria
- AI Models
- Asynchronous Programming
- Parallel Execution
---

# Example Run


```python
from dria.client import Dria
from dria.factory import MagPie
from dria.models import Model
from dria.batches import ParallelSingletonExecutor
import asyncio

async def batch():
    dria_client = Dria()
    singleton = MagPie()
    executor = ParallelSingletonExecutor(dria_client, singleton)
    executor.set_models([Model.GPT4O_MINI, Model.GEMINI_15_FLASH, Model.MIXTRAL_8_7B])
    executor.load_instructions([{ "prompt": "What is the capital of France?" }, { "prompt": "What is the capital of Germany?" }])
    return await executor.run()

def main():
    results = asyncio.run(batch())
    print(results)

if __name__ == "__main__":
    main()
```