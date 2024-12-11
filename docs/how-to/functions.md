---
categories:
- Workflows
description: Explore Dria Nodes functions for built-in and custom tools, including
  HTTP requests and workflows for seamless automation.
tags:
- Dria Nodes
- Workflow Automation
- Custom Functions
- HTTP Requests
- Generative Steps
---

# Functions

Dria Nodes provides several built-in tools that are included in your workflow by default. 
Selecting `Operator.FUNCTION_CALLING` will pick a tool from the list of built-in tools and execute it based on the instruction provided.

Example Step:

```python
builder.generative_step(
    id="task_id",
    prompt="What are the current prices of $AAPL and $GOOGL?",
    operator=Operator.FUNCTION_CALLING,
    outputs=[Write.new("result")]
)
```

Step above will select the `Stock` tool and execute it based on the instruction provided.

See [workflows](workflows.md) for available built-in tools.

# Custom Functions

Dria enables you to create custom functions (tools) that can be used in your workflows. 
These functions can be used to perform custom operations that are not natively supported by Dria.

Dria supports two types of custom functions:

- `CustomTool`: A pydantic model that can be used in your workflows.

`CustomTool` will not be executed by Dria. Instead, it will be returned as a function call in the workflow output.

- `HttpRequestTool`: An HTTP request tool that can be used to make HTTP requests in your workflows. 

`HttpRequestTool` will be executed by Dria and the result will be returned in the workflow output.

#### CustomTool

To create a custom function, you need to create a class that inherits from `CustomTool` and implement the `execute` method.

```python
from dria_workflows import CustomTool
from pydantic import Field

class SumTool(CustomTool):
    name: str = "calculator"
    description: str = "A tool sums integers"
    lhs: int = Field(0, description="Left hand side of sum")
    rhs: int = Field(0, description="Right hand side of sum")

    def execute(self, **kwargs):
        return self.lhs + self.rhs
```

`name` and `description` are required fields that describe the custom function. 
For the rest of your custom function, you can define any number of fields that you need.
If field has a default value, it means it's a required field.

To incorporate the custom function into your workflow, simple call `add_custom_tool` method on the `WorkflowBuilder` instance.

```python
builder = WorkflowBuilder()
builder.add_custom_tool(SumTool())
```

This would add the custom function to the list of available functions in your workflow.

```python
builder.generative_step(
    id="sum",
    prompt=f"What is {lhs} + {rhs}?",
    operator=Operator.FUNCTION_CALLING_RAW,
    outputs=[Write.new("call")]
)
```

Steps that incorporate custom functions should use `Operator.FUNCTION_CALLING_RAW` as the operator. 
This would force Dria Nodes to return the function call without executing it.

Below is a full example of a workflow that sums two numbers using a custom function:

```python
import asyncio
from typing import List
from pydantic import BaseModel, Field
from dria_workflows import Workflow, WorkflowBuilder, Operator, Edge, Write, CustomTool
from dria.factory.workflows.template import SingletonTemplate
from dria.models import TaskResult
from dria import DriaDataset, DatasetGenerator, Model

class SumTool(CustomTool):
    """
    A custom tool to perform summation of two integers.
    """
    name: str = "calculator"
    description: str = "A tool that sums two integers."
    lhs: int = Field(0, description="Left-hand operand for summation")
    rhs: int = Field(0, description="Right-hand operand for summation")

    def execute(self, **kwargs) -> int:
        """
        Execute the summation operation.

        Returns:
            int: The sum of lhs and rhs
        """
        return self.lhs + self.rhs


class SummationOutput(BaseModel):
    """
    Schema for the output of the summation workflow.
    """
    query: str = Field(..., description="The function calling query.")
    result: int = Field(..., description="The result of the summation.")


class Summation(SingletonTemplate):
    """
    Workflow for executing a summation operation and handling function calls.
    """
    # Input fields
    prompt: str = Field(..., description="Input prompt for the workflow")

    # Output schema
    OutputSchema = SummationOutput

    def workflow(self) -> Workflow:
        """
        Creates the summation workflow.

        Returns:
            Workflow: A constructed workflow for summation
        """
        # Set default values for the workflow
        max_tokens = getattr(self.params, "max_tokens", 1000)
        builder = WorkflowBuilder()

        # Add custom summation tool to the workflow
        builder.add_custom_tool(SumTool())
        builder.set_max_tokens(max_tokens)

        # Define the generative step for function calling
        builder.generative_step(
            prompt=self.prompt,
            operator=Operator.FUNCTION_CALLING_RAW,
            outputs=[Write.new("calculation_result")]
        )

        # Define the workflow flow structure
        flow = [Edge(source="0", target="_end")]
        builder.flow(flow)

        # Set the final return value of the workflow
        builder.set_return_value("calculation_result")
        return builder.build()

    def callback(self, result: List[TaskResult]) -> List[SummationOutput]:
        """
        Parses the workflow results into validated output objects.

        Args:
            result: List of TaskResult objects

        Returns:
            List[SummationOutput]: List of validated summation outputs
        """
        outputs = []
        for task_result in result:
            for calculation in task_result.parse():
                outputs.append(
                    SummationOutput(
                        query=task_result.result,
                        result=calculation.execute([SumTool])
                    )
                )
        return outputs

instructions = [
    {
        "prompt": "What is 10212 + 12677?"
    }
]

my_dataset = DriaDataset("summation_test", "a test dataset", Summation.OutputSchema)
generator = DatasetGenerator(dataset=my_dataset)

asyncio.run(
    generator.generate(
        instructions,
        Summation,
        [
            Model.GPT4O,
        ],
    )
)

print(my_dataset.get_entries())

```

#### HttpRequestTool

`HttpRequestTool` is a tool that can be used to make HTTP requests in your workflows. 
Unlike `CustomTool`, `HttpRequestTool` will be executed by Dria Nodes and the result will be returned in the workflow output.

To create an `HttpRequestTool`, you need to create a class that inherits from `HttpRequestTool` and implement the `execute` method.

```python
from dria_workflows import HttpRequestTool, HttpMethod
class PriceFeedTool(HttpRequestTool):
    name: str = "PriceFeedRequest"
    description: str = "Fetches price feed from Gemini API"
    url: str = "https://api.gemini.com/v1/pricefeed"
    method: HttpMethod = HttpMethod.GET
```

An `HttpRequestTool` requires the following fields:

- `name`: The name of the tool.
- `description`: A description of the tool.
- `url`: The URL to make the HTTP request to.
- `method`: The HTTP method to use for the request.
- `headers`: Optional headers to include in the request.
- `body`: Optional body to include in the request.

A `HttpRequestTool` can be added to the workflow in the same way as a `CustomTool`. 
Here is an example of a workflow that fetches cryptocurrency prices using an `HttpRequestTool`:

```python
class PriceFeedTool(HttpRequestTool):
    name: str = "PriceFeedRequest"
    description: str = "Fetches price feed from Gemini API"
    url: str = "https://api.gemini.com/v1/pricefeed"
    method: HttpMethod = HttpMethod.GET


def workflow():
    """
    Create a workflow to get cryptocurrency prices
    :return:
    """

    builder = WorkflowBuilder()
    builder.add_custom_tool(PriceFeedTool())

    builder.generative_step(
        id="get_prices",
        prompt=f"What is the BTC/USDT parity?",
        operator=Operator.FUNCTION_CALLING,
        outputs=[Write.new("prices")]
    )

    flow = [
        Edge(source="get_prices", target="_end")
    ]
    builder.flow(flow)
    builder.set_return_value("prices")
    return builder.build()
```