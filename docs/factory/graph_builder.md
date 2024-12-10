---
categories:
- Data Generation
description: GenerateGraph extracts ontological relationships from text, creating
  a graph of related concepts and connections.
tags:
- graph generation
- ontology extraction
- data structure
- machine learning
- AI relationships
---

# GenerateGraph

## Overview
GenerateGraph is a singleton template designed to extract ontological relationships from a given context. It processes text to identify concepts and their relationships, generating a graph-like structure of related terms and their connections.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| context | str | The context from which to extract the ontology of terms |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| graph | GraphRelation | The generated graph relation containing node_1, node_2, and edge |
| model | str | The AI model used for generation |

### GraphRelation Schema
| Field | Type | Description |
|-------|------|-------------|
| node_1 | str | A concept from extracted ontology |
| node_2 | str | A related concept from extracted ontology |
| edge | str | Relationship between the two concepts |

#### Usage

GenerateGraph instance can be used in data generation as follows:

```python
from dria.factory import GenerateGraph

my_dataset = DriaDataset(
    name="generate_graph",
    description="A dataset for ontology extraction",
    schema=GenerateGraph.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
{
   "graph":[
      {
         "edge":"Machine learning is a subfield within the broader field of Artificial Intelligence.",
         "node_1":"Artificial Intelligence",
         "node_2":"machine learning"
      },
      {
         "edge":"Deep learning is another subfield of Artificial Intelligence that focuses on deep neural networks.",
         "node_1":"Artificial Intelligence",
         "node_2":"deep learning"
      },
      {
         "edge":"Deep learning is a specific approach within machine learning that uses deep neural networks to model complex patterns in data.",
         "node_1":"machine learning",
         "node_2":"deep learning"
      },
      {
         "edge":"Neural networks are crucial components used in the construction of deep learning systems.",
         "node_1":"neural networks",
         "node_2":"deep learning systems"
      }
   ],
   "model":"qwen2.5:32b-instruct-fp16"
}
```