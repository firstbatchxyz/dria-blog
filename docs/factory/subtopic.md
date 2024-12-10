---
categories:
- Workflows
description: Explore the SubTopicPipeline class for generating recursive subtopics
  in AI. Customize depth and enhance topic research efficiency.
tags:
- AI
- Subtopics
- Topic Generation
- Artificial Intelligence
- Workflow
---

# GenerateSubtopics

## Overview
GenerateSubtopics is a singleton template that generates subtopics for a given main topic. It creates a workflow that processes a topic and breaks it down into relevant subtopics using AI generation.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| topic | str | Main topic to generate subtopics for |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| topic | str | The original main topic (echoed from input) |
| subtopic | str | Generated subtopic of the main topic |
| model | str | The AI model used for generation |

#### Usage

GenerateSubtopics instance can be used in data generation as follows:

```python
from dria.factory import GenerateSubtopics

my_dataset = DriaDataset(
    name="GenerateSubtopics",
    description="A dataset for generating topic subtopics",
    schema=GenerateSubtopics.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected Output

```json
[
  {
    "topic": "rust language",
    "subtopic": "Ownership and Borrowing Concepts",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Memory Safety Without Garbage Collection",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Zero-Cost Abstractions in Systems Programming",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Concurrent Programming with Async/Await",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Pattern Matching and Algebraic Data Types",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Performance and Low-Level Control",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "WebAssembly and Cross-Platform Development",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Error Handling with Result and Option Types",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Macros and Meta-Programming Techniques",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Safety and Compile-Time Guarantees",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Cargo Package Management System",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Interoperability with C and Other Languages",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Functional Programming Paradigms",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  },
  {
    "topic": "rust language",
    "subtopic": "Systems and Application Programming Use Cases",
    "model": "anthropic/claude-3-5-haiku-20241022:beta"
  }
]
```