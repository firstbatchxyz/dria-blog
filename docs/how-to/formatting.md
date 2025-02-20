---
categories:
- Applied AI
description: Learn to use the Formatter class for converting datasets into training
  formats suitable for various AI models.
tags:
- Formatter
- Data Formatting
- AI Training
- Hugging Face
- Dria Network
---

# Formatter

The `Formatter` class is used to convert a dataset into a format that can be used by a specific trainer. 

Data generated by Dria Network can be transformed into training-ready data using `Formatter`

## Format Types

The `Formatter` class supports the following format types:

- Standard
- Conversational

and following subtypes for each format type:

1. LANGUAGE_MODELING
2. PROMPT_ONLY
3. PROMPT_COMPLETION
4. PREFERENCE
5. UNPAIRED_PREFERENCE


## Standard Format Types

For standard format types, import:

```python
from dria.utils import FieldMapping, DataFormatter, FormatType
```

and create a mapping for the data keys to the formatted data keys.

```python
FieldMapping( # field mapping, for mapping data keys to formatted data keys
    prompt="instruction",
    completion="generation", 
    label="score",  
    )
```

and run

```python
formatted_data = DataFormatter().format(
    data, 
    FormatType.STANDARD_UNPAIRED_PREFERENCE, # format type
    FieldMapping(
        prompt="instruction", # map instruction to prompt
        completion="generation", # map generation to completion
        label="score",  # map score to label
        )
    )
```

## Conversational Format Types

For conversational format types, import:

```python
from dria.utils import ConversationMapping, FieldMapping, DataFormatter, FormatType
```

Create a conversation mapping for the data keys to the formatted data keys.

```python
mapping = ConversationMapping(
    field="dialogue",
    conversation=FieldMapping(
        prompt="question", chosen="answer", rejected="failed"
    ),
)
```

and run

```python
formatted_data = DataFormatter().format(
    data, 
    FormatType.CONVERSATIONAL_LANGUAGE_MODELING, # format type
    ConversationMapping(
    field="dialogue",
    conversation=FieldMapping(
        prompt="question", chosen="answer", rejected="failed"
        ),
    )
)
```

## Usage

In this example, we will use the `Formatter` class to convert the generated data from `InstructionBacktranslation` into the `STANDARD_UNPAIRED_PREFERENCE` format.

```python
from dria.client import Dria
from dria.factory import InstructionBacktranslation
from dria.models import Model
from dria.batches import ParallelSingletonExecutor
from dria.utils import FieldMapping, DataFormatter, FormatType
import asyncio


async def batch():
    dria_client = Dria()
    singleton = InstructionBacktranslation()
    executor = ParallelSingletonExecutor(dria_client, singleton)
    executor.set_models([Model.OPENAI, Model.OLLAMA, Model.GEMINI])
    executor.load_instructions(
        [
            {
                "instruction": "What is 3 times 20?",
                "generation": "It's 60.",
            },
            {
                "instruction": "What is 3 times 20?",
                "generation": "It's 59.",
            },
        ]
    )
    return await executor.run()


def main():
    results = asyncio.run(batch())
    # Lambda to update scores to boolean
    update_scores = lambda data: [
        {**item, 'score': int(item['score']) > 3} for item in data
    ]
    updated_results = update_scores(results)
    formatted_data = DataFormatter().format(
        updated_results, 
        FormatType.STANDARD_UNPAIRED_PREFERENCE, 
        FieldMapping(
            prompt="instruction",
            completion="generation", 
            label="score",  
            )
    )

    print(formatted_data)


if __name__ == "__main__":
    main()

```


```json
[
   {
      "prompt":"What is 3 times 20?",
      "completion":"It's 60.",
      "label":true
   },
   {
      "prompt":"What is 3 times 20?",
      "completion":"It's 59.",
      "label":false
   }
]
```

## HuggingFace TRL Expected Dataset Formats

HuggingFace's TRL is a framework to train transformer language models with Reinforcement Learning, from the Supervised Fine-tuning step (SFT), Reward Modeling step (RM) to the Proximal Policy Optimization (PPO) step.

Dria allows you to convert the generated data into the expected dataset [format](https://huggingface.co/docs/trl/dataset_formats) for each trainer in the TRL framework. 
Enabling seamless plug-n-play with HuggingFace's TRL.

---

| Trainer               | Expected Dataset Type                                       |
|-----------------------|------------------------------------------------------------|
| **BCOTrainer**        | `FormatType.STANDARD_UNPAIRED_PREFERENCE`                  |
| **CPOTrainer**        | `FormatType.STANDARD_PREFERENCE` |
| **DPOTrainer**        | `FormatType.STANDARD_PREFERENCE`|
| **GKDTrainer**        | `FormatType.STANDARD_PROMPT_COMPLETION`                    |
| **IterativeSFTTrainer** | `FormatType.STANDARD_UNPAIRED_PREFERENCE`                |
| **KTOTrainer**        | `FormatType.STANDARD_UNPAIRED_PREFERENCE` or `FormatType.STANDARD_PREFERENCE` |
| **NashMDTrainer**     | `FormatType.STANDARD_PROMPT_ONLY`                          |
| **OnlineDPOTrainer**  | `FormatType.STANDARD_PROMPT_ONLY`                          |
| **ORPOTrainer**       | `FormatType.STANDARD_PREFERENCE`|
| **PPOTrainer**        | `FormatType.STANDARD_LANGUAGE_MODELING`|
| **RewardTrainer**     | `FormatType.STANDARD_PREFERENCE`|
| **SFTTrainer**        | `FormatType.STANDARD_LANGUAGE_MODELING`                    |
| **XPOTrainer**        | `FormatType.STANDARD_PROMPT_ONLY`                          |