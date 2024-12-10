---
categories:
- Applied AI
description: 'Explore StructRAG: a hybrid approach to knowledge restructuring for
  enhancing LLM reasoning capabilities via structured information.'
tags:
- StructRAG
- Knowledge Restructuring
- Hybrid Information
- LLM
- Machine Learning
---

# StructRAG

## Knowledge Restructuring

Hybrid Router's decisions is used to decide the format of the structured information. 

```python
import json
import os
from dria.factory import (
    StructRAGGraph,
    StructRAGCatalogue,
    StructRAGAlgorithm,
    StructRAGTable
)
from dria.client import Dria
from dria.models import Model
import asyncio
from itertools import chain
from typing import List, Optional

dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])

async def evaluate():
    score_complexity = StructRAGCatalogue()
    instructions = [
        "Boil water in a kettle",
        "Write a research paper on quantum physics",
        "Tie your shoelaces",
        "Develop a machine learning algorithm",
        "Make a sandwich"
    ]
    res = await dria.execute(
        Task(
            workflow=score_complexity.workflow(instructions=instructions).model_dump(),
            models=[Model.GPT40_MINI],
        )
    )
    return score_complexity.parse_result(res)

def main():
    result = asyncio.run(evaluate())
    print(result)

if __name__ == "__main__":
    main()
```

## References
- [StructRAG: Boosting Knowledge Intensive Reasoning of LLMs via Inference-time Hybrid Information Structurization](https://arxiv.org/abs/2410.08815)