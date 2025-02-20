---
categories:
- Software Engineering
description: Generate code dynamically with powerful Singleton classes for code generation
  and iteration in multiple programming languages.
tags:
- code generation
- Singleton pattern
- AI coding
- Python
- software development
---

# GenerateCode

### Overview
This implementation provides two Singleton classes for code generation and iteration: `GenerateCode` and `IterateCode`. These classes are designed to generate and iterate code based on given instructions in specified programming languages.

> ⚠️ `GenerateCode` works best with coder models. You can use them with `Model.CODER`or specifying with `Model.QWEN2_5_CODER_1_5B`.

### Inputs
| Field | Type | Description |
|-------|------|-------------|
| instruction | str | The instruction to generate code for |
| language | str | The programming language to generate code for |

### Outputs
| Field | Type | Description |
|-------|------|-------------|
| instruction | str | The original instruction (echoed from input) |
| language | str | The programming language used |
| code | str | The generated code |
| model | str | The AI model used for generation |

### Usage

```python
from dria.factory import GenerateCode

generator = GenerateCode(
    instruction="Write a function to calculate fibonacci numbers",
    language="python"
)
```

### Expected output

```json
{
   "instruction":"Write a function to calculate the factorial of a number",
   "language":"python",
   "code":"def factorial(n):\n    \"\"\"\n    Calculate the factorial of a non-negative integer n.\n    \n    Args:\n    n (int): A non-negative integer whose factorial is to be calculated.\n    \n    Returns:\n    int: The factorial of the input number.\n    \n    Raises:\n    ValueError: If n is negative.\n    \"\"\"\n    # Check if the input is a non-negative integer\n    if not isinstance(n, int) or n < 0:\n        raise ValueError(\"Input must be a non-negative integer.\")\n    \n    # Initialize the result to 1 (since 0! = 1)\n    result = 1\n    \n    # Calculate the factorial using a loop\n    for i in range(1, n + 1):\n        result *= i\n    \n    return result\n\n# Example usage:\ntry:\n    print(factorial(5))  # Output: 120\nexcept ValueError as e:\n    print(e)",
   "model":"qwen2.5-coder:1.5b"
}
```