---
categories:
- Applied AI
description: Explore an example of asynchronous batch processing using the Dria library
  with multiple AI models.
tags:
- Dria
- Python
- Asynchronous
- AI Models
- Batch Processing
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