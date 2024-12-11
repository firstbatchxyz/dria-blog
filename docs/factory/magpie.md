---
categories:
- Workflows
description: MagPie is a versatile template for generating dialogues between personas
  while managing conversation turns efficiently.
tags:
- dialogue generation
- AI personas
- conversation management
- data generation
- natural language processing
---

# MagPie

## Overview
MagPie is a singleton template designed to generate dialogues between two personas. It facilitates the creation of conversational exchanges by managing turns between an instructor and a responder, with configurable number of dialogue turns.

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| instructor_persona | str | Persona of the instructor who initiates the dialogue |
| responding_persona | str | Persona of the responder who replies to the instructor |
| num_turns | conint(ge=1) | Number of conversation turns (must be greater than or equal to 1) |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| dialogue | List[DialogueTurn] | List of dialogue turns, each containing instructor and responder messages |
| model | str | The AI model used for generation |

### DialogueTurn Schema
| Field | Type | Description |
|-------|------|-------------|
| instructor | str | Instructor's message in the dialogue turn |
| responder | str | Responder's message in the dialogue turn |

#### Usage

MagPie instance can be used in data generation as follows:

```python
from dria.factory import MagPie

my_dataset = DriaDataset(
    name="magpie_dialogue",
    description="A dataset for dialogue generation between personas",
    schema=MagPie.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)
```

### Expected output

```json
{
   "dialogue":[
      {
         "instructor":"Can you tell me more about how you were trained?  What kind of data did you learn from? \n"
      },
      {
         "responder":"That's a fascinating question! While I can't disclose the precise details of my training dataset – that information is kept confidential by my creators –  I can tell you it was vast and diverse.  \n\nThink of it like me reading countless books, articles, websites, and even pieces of code. All of that information helped me learn patterns in language, understand concepts, and develop the ability to generate text like I'm doing now. \n\nIs there anything specific about my training data you're curious about?  Perhaps the types of topics or the languages involved?  I can try to give you some general insights. \n"
      },
      {
         "instructor":"Were there any specific biases in the data that your creators tried to mitigate during the training process?  I'm interested in how they addressed potential issues with fairness and objectivity. \n"
      },
      {
         "responder":"That's a very important question! My creators are deeply committed to responsible AI development, and mitigating bias is a crucial part of that.  \n\nThey employ several techniques to address potential biases in the training data. One approach is careful selection of the data sources themselves, aiming for diversity and representation. \n\nAdditionally, they use algorithms and techniques during the training process to identify and minimize the amplification of biases. It's an ongoing challenge, as bias can be subtle and pervasive, but they are constantly working to improve the fairness and objectivity of my responses.  \n"
      },
      {
         "instructor":"That's reassuring to hear.  Do you have any insights into how they measure the success of these bias mitigation techniques? \n"
      },
      {
         "responder":"That's a great question! Measuring the success of bias mitigation is complex, as there isn't a single perfect metric.  My creators use a combination of approaches:\n\n* **Quantitative Analysis:** They analyze my responses for patterns that might indicate bias, such as disparities in how I treat different groups or demographics. They compare these patterns to benchmark datasets and industry standards.\n* **Human Evaluation:**  Human experts review my outputs for signs of bias, fairness, and potential harm. Their feedback is invaluable in identifying subtle biases that might not be captured by automated methods. \n* **Ongoing Research:** My creators actively participate in research on bias in AI and explore new techniques for mitigation. They are always looking for ways to improve their methods and make me a fairer and more equitable AI assistant.  \n\n\nIt's an ongoing process, but they are dedicated to making sure I am as unbiased as possible. \n"
      }
   ],
   "model":"gemma2:9b-instruct-fp16"
}
```

#### References
- [Distilabel MagPie](https://distilabel.argilla.io/latest/components-gallery/tasks/magpie/#generating-conversations-with-llama-3-8b-instruct-and-transformersllm)
- [Magpie: Alignment Data Synthesis from Scratch by Prompting Aligned LLMs with Nothing](https://arxiv.org/html/2406.08464v1)