---
categories:
- Applied AI
description: 'Explore StructRAG: an innovative framework enhancing LLMs for knowledge-intensive
  reasoning by structuring information for better accuracy.'
tags:
- StructRAG
- LLMs
- Artificial Intelligence
- Knowledge Reasoning
- Data Structuring
---

# StructRag

Implements the StructRAG framework, a novel retrieval-augmented generation (RAG) approach aimed at enhancing 
large language models (LLMs) for knowledge-intensive reasoning tasks. Unlike conventional RAG methods, 
StructRAG addresses the challenge of scattered, noisy information in such tasks by employing cognitive-inspired 
techniques. It automatically identifies an optimal structure type for a given task, restructures original documents 
into this format, and conducts inference on the structured information, improving accuracy and reasoning capabilities. 
Experiments demonstrate StructRAG's effectiveness across various complex knowledge-based tasks, where it achieves 
state-of-the-art results.

## Module Overview

This module explains the pipeline to recreate **DPO data for Hybrid Router**. 

You can find generated data and a post-trained `Qwen2.5-7b-Instruct` model on huggingface:

[Link to dataset](https://huggingface.co/datasets/andthattoo/router-dpo)

[Link to model](https://huggingface.co/andthattoo/Qwen2.5-7B-StructRAG-router)

#### StructRAGSynthesize

Purpose: Initializes and structures workflows for generating initial document representations and extracts key document information to support reasoning tasks.

Usage: Utilized in the initial phase to transform raw information into structured knowledge units that are relevant to the given topic.

#### StructRAGSimulate

Usage: Applied after StructRAGSynthesize to simulate responses, enabling the framework to test solution accuracy based on structured data.

Purpose: Conducts simulations to generate solutions by processing document information and queries, preparing structured data for the StructRAG reasoning task.

#### StructRAGJudge

Purpose: Evaluates the relevance and correctness of generated solutions (from StructRAGSimulate step) by processing simulation data and ordering solutions based on model evaluation.

Usage: Used in the final phase to validate and refine StructRAG outputs, providing quality-controlled answers based on structured data analysis.


```python
import json
import os
from dria.factory import (
    StructRAGSynthesize,
    StructRAGSimulate,
    StructRAGJudge,
)
from dria.client import Dria
from dria.models import Model
from dria.batches import ParallelSingletonExecutor
import asyncio
from itertools import chain
from typing import List, Optional

dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])


async def batch(instructions, singleton_instance, models: List[Model]):
    dria_client = Dria()
    singleton = singleton_instance()
    executor = ParallelSingletonExecutor(dria_client, singleton, batch_size=2000)
    executor.set_models(models)
    executor.load_instructions(instructions)
    return await executor.run()


def batch_run(instructions, instance, models: Optional[List[Model]] = None):
    print(instance.__name__)
    print("Number of instructions: ", len(instructions))
    if not models:
        models = [Model.GEMINI_15_PRO, Model.QWEN2_5_32B_FP16, Model.GPT4O]

    results = asyncio.run(batch(instructions, instance, models))
    with open(f"results_{instance.__name__}.json", "w") as f:
        f.write(json.dumps(results, indent=2))


if __name__ == "__main__":


    # Synthesize

    seeds = ['History', 'Psychology', 'Economics', 'Political Science', 'Linguistics', 'Astronomy', 'Chemistry', 'Biology', 'Environmental Science', 'Culinary Arts', 'Architecture', 'Wildlife', 'Computers', 'Food', 'Physics', 'Communication', 'Music', 'Sociology', 'Art', 'Modern Art', 'Mechanical Physics', 'Mathematics', 'Philosophy', 'Geography', 'Anthropology', 'Literature', 'Theater', 'Film', 'Education', 'Business', 'Engineering', 'Medicine', 'Law', 'Public Health', 'Data Science', 'Artificial Intelligence', 'Robotics', 'Genetics', 'Neuroscience', 'Astrophysics', 'Oceanography', 'Meteorology', 'Geology', 'Agronomy', 'Zoology', 'Botany', 'History', 'Psychology', 'Economics', 'Political Science', 'Linguistics', 'Astronomy', 'Chemistry', 'Biology', 'Environmental Science', 'Culinary Arts', 'Architecture', 'Wildlife', 'Computers', 'Food', 'Physics', 'Communication', 'Music', 'Sociology', 'Art', 'Modern Art', 'Mechanical Physics']
    batch_run(
        [{"seed": seed} for seed in seeds],
        StructRAGSynthesize,
        [
            Model.GEMINI,
            Model.GPT4O,
            Model.QWEN2_5_32B_FP16,
            Model.LLAMA3_1_8B_FP16,
            Model.LLAMA3_1_70B,
        ],
    )

    # Simulate
    with open(f"results_{StructRAGSynthesize.__name__}.json", "r") as f:
        data = json.load(f)
    datax = list(chain(*data))

    batch_run(
        [
            {"query": d["query"], "documents_info": d["documents_info"]}
            for d in datax
        ],
        StructRAGSimulate,
        [
            Model.GEMINI_15_PRO,
            Model.GEMINI_15_FLASH,
            Model.GPT4O,
            Model.QWEN2_5_32B_FP16,
            Model.LLAMA3_1_8B_FP16,
            Model.LLAMA3_1_70B
        ],
    )

    # Judge
    
    with open(f"results_{StructRAGSimulate.__name__}.json", "r") as f:
        data = json.load(f)

    batch_run(
        [
            {
                "query": d["query"],
                "documents_info": d["documents_info"],
                "solutions": d["solutions"],
            }
            for d in data
        ],
        StructRAGJudge,
        [
            Model.GEMINI,
            Model.OPENAI,
            Model.QWEN2_5_32B_FP16,
        ]
    )
```

## References
- [StructRAG: Boosting Knowledge Intensive Reasoning of LLMs via Inference-time Hybrid Information Structurization](https://arxiv.org/abs/2410.08815)