---
categories:
- Applied AI
description: Rank instructions by complexity with ScoreComplexity using GEMMA2 model.
  Ideal for evaluating task difficulty in NLP.
tags:
- complexity
- natural language processing
- task ranking
- AI models
- instruction evaluation
---

# ScoreComplexity

`ScoreComplexity` is a `Singleton` task that ranks a list of instructions based on their complexity.

#### Inputs
- instructions (`List[str]`): A list of instructions to be ranked.

#### Outputs
- scores (`str`): A string containing the complexity scores for each instruction.

#### Expected output

```json
[
   {
      "instruction":"Boil water in a kettle",
      "score":3,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Write a research paper on quantum physics",
      "score":5,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Tie your shoelaces",
      "score":4,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Develop a machine learning algorithm",
      "score":5,
      "model":"llama3.1:8b-instruct-fp16"
   },
   {
      "instruction":"Make a sandwich",
      "score":2,
      "model":"llama3.1:8b-instruct-fp16"
   }
]
```

#### References
- [ComplexityScorer Distilabel](https://distilabel.argilla.io/latest/components-gallery/tasks/complexityscorer)
- [What Makes Good Data for Alignment? A Comprehensive Study of Automatic Data Selection in Instruction Tuning](https://arxiv.org/abs/2312.15685)