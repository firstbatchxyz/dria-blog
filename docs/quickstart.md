---
categories:
- Workflows
description: Quick start guide to create a dialogue using Dria SDK with Python. Learn
  to implement a math teacher-student interaction.
tags:
- Dria SDK
- Python
- Dialogue Generation
- AI Models
- Quick Start
---

# Quick Start

> In order to follow this guide, you need to [install](installation.md) Dria SDK.


Let's get started with Dria SDK by creating a dialogue between a math teacher and a student. 

Import the necessary modules and create a `Dria` instance.

```python
import os
import asyncio
from dria.factory import MagPie
from dria.client import Dria
from dria.models import Task, Model
import json

dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])
```

Define a function to generate a dialogue between two personas using the `MagPie` task.

```python
async def run_task():
    magpie = MagPie()
    res = await dria.execute(
        Task(
            workflow=magpie.workflow(
                instructor_persona="A curious math student.",
                responding_persona="A grumpy math Professor assistant with short, snappy answers.",
                num_turns=3
            ),
            models=[Model.GPT4O_MINI],
        )
    )
    return magpie.parse_result(res)
```

Now wrap the `run_task` function in a main function to run the task and print the result.

```python
def main():
    result = asyncio.run(evaluate())
    print(json.dumps(result, indent=4))

    
if __name__ == "__main__":
    main()
```

And that's it! Run the script, and you should see a dialogue between the two personas.

```json
[
    {
        "dialogue": [
            {
                "instructor": "Can you explain why the square root of a negative number is imaginary? I'm really curious about that!",
                "responder": "Because it doesn't exist on the number line. We define the square root of negative numbers as imaginary to fill that gap. Simple enough?"
            },
            {
                "instructor": "So, if imaginary numbers help fill the gap, what are they actually used for in real-world applications?",
                "responder": "They're used in engineering, physics, and even signal processing. Ever heard of alternating current? That\u2019s imaginary math at work."
            },
            {
                "instructor": "Wow, that's fascinating! So, imaginary numbers have real-world applications. Can you give me a specific example of how they are used in physics?",
                "responder": "Sure, take electrical engineering. They use imaginary numbers in calculating impedance in AC circuits. Helps simplify complex calculations. Clear enough?"
            }
        ],
        "model": "gpt-4o-mini"
    }
]
```


For more, check out Dria Factory tab, or go cracked mode and see how you can build custom pipelines and task!