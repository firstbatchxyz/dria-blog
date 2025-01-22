---
categories:
- Data Generation
description: Generate complex multi-hop questions from three document chunks with
  MultiHopQuestion, including answers and AI model used.
tags:
- Multi-hop questions
- Question generation
- AI models
- Natural language processing
- Data generation
---

# MultiHopQuestion

## Overview
MultiHopQuestion is a singleton template that generates multi-hop questions from three document chunks. It creates a set of questions with increasing complexity (1-hop, 2-hop, and 3-hop) along with their corresponding answers based on the provided input documents.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| chunks | List[str] | A list of exactly three document chunks used as source material for question generation |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| one_hop | str | A single-step (1-hop) question based on the input documents |
| two_hop | str | A two-step (2-hop) question requiring information from multiple documents |
| three_hop | str | A three-step (3-hop) question requiring complex reasoning across all documents |
| answer | str | The answer to the generated questions |
| model | str | The AI model used for generation |

#### Usage

MultiHopQuestion instance can be used in data generation as follows:

```python
from dria.factory import MultiHopQuestion

my_dataset = DriaDataset(
    name="MultiHopQuestion",
    description="A dataset for multi-hop question generation",
    schema=MultiHopQuestion.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected Output

```json
[
  {
    "1-hop": "Who was William de Ros's favorite son, as indicated by the land he inherited?",
    "2-hop": "Which of William de Ros's sons received a portion of his patrimony, overriding family duty and convention, according to G. L. Harriss?",
    "3-hop": "Who was described as the favorite son and also benefited from his father's decision to override family duty and convention regarding the inheritance, as mentioned by both Charles de Ross and G. L. Harriss?",
    "answer": "William de Ros's third son, Robert",
    "model": "mixtral:8x7b"
  }
]
```

#### References 
- [Multi-hop Question Answering](https://arxiv.org/abs/1809.09600) 
- [Explainable Multi-hop Question Generation: An End-to-End Approach without Intermediate Question Labeling](https://arxiv.org/pdf/2404.00571)