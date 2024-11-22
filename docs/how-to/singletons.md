---
categories:
- Workflows
description: Explore singletons for streamlined task automation in Python. Learn to
  create and implement custom singletons for specific functions.
tags:
- singleton
- task automation
- Python
- custom workflows
- software development
---

# Singletons

Singletons are a set of pre-built tasks that are designed to perform specific functions. 
They are called singletons because they are designed to be used as single instances that perform a specific task. 
Singletons are a powerful tool that can be used to quickly and easily perform a wide range of tasks without having to write custom code.

To create a singleton, see the [Custom Singletons](#custom-singletons) section.

In order to use a singleton, you simply need to import the singleton class and create a `Task` instance with it.
Here is an example of how to use a singleton to perform a simple task:

Import the singleton class

```python
from dria.factory import EvolveInstruct
```

Create an instance of `Task` using the singleton

```python
evolve_instruct = EvolveInstruct()
original_prompt = "Explain the concept of photosynthesis."
task = Task(
    workflow=evolve_instruct.workflow(prompt=original_prompt, mutation_type="DEEPEN"),
    models=[Model.GEMMA2_9B_FP16],
)
```

Each `Singleton` has two abstract methods:

1. `workflow`: This method returns the workflow that the singleton will execute. The workflow is a series of steps that the singleton will perform in order to complete its task.
2. `parse_result`: This method takes the result of the task and parses it into a human-readable format.

Find all available singletons in the `dria.factory` module.


### Custom Singletons

Dria SDK enables the creation of custom singletons. This is useful when factory singletons do not meet your requirements.
To create a custom singleton, you need to create a new class that inherits from the `SingletonTemplate` class.

Ideal folder structure for custom singletons is as follows:
```
- custom_singleton
    - __init__.py
    - prompt.md
    - task.py
```

The `SingletonTemplate` class has two abstract methods:

1. `workflow`: This method should return the workflow that the singleton will execute.
2. `parse_result`: This method should take the result of the task and parse it into a human-readable format.


```python
from dria.models import TaskResult
from dria.factory.workflows.template import SingletonTemplate
from typing import List


class MyCustomSingleton(SingletonTemplate):
    def workflow(self, **kwargs):
        pass
    
    def parse_result(self, result: List[TaskResult]):
        pass
```

In order to clarify, let's create a singleton that returns string in reversed.

Prompt file `prompt.md`:
``` 
Reverse the given string
{{string}}
```

> Variables in prompt file should be enclosed in double curly braces `{{ }}`.


```python
from dria_workflows import *  # Import all necessary classes to create a workflow
from dria.factory.utilities import get_abs_path  # Used to get the absolute path of the prompt file
from dria.models import TaskResult
from dria.factory.workflows.template import SingletonTemplate
from typing import List


class ReverseStringSingleton(SingletonTemplate):
    def workflow(self, string: str):
        
        # Create a workflow builder, uses kwargs to map variables to prompts
        builder = WorkflowBuilder(string=string)
        
        builder.generative_step(
            id="reverse_string",
            path=get_abs_path("prompt.md"),
            operator=Operator.GENERATION,
            outputs=[Write.new("reversed_string")],  # we want the generative step to write output to 'reversed_string' key in memory
        )
        
        # Define the flow of your workflow
        flow = [Edge(source="reverse_string", target="_end")]
        builder.flow(flow)
        
        # Set the return value of your workflow
        builder.set_return_value("reversed_string")  # Read the value of 'reversed_string' from memory and return it
        
        # Build your workflow
        return builder.build()
        
    
    def parse_result(self, result: List[TaskResult]):
        return [
            {"reversed": r.result, "original": r.task_input["string"]}  for r in result
        ]
```