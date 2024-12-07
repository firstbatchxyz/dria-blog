---
categories:
- Workflows
description: Learn about Singletons in Dria, including how to use and create your
  own for efficient task handling with Pydantic validation.
tags:
- Singletons
- Dria
- Pydantic
- Task Management
- Data Generation
---

# Singletons

Singletons are pre-built task templates that perform specific functions using a standardized structure. 
Each singleton is designed as a single instance that handles a specific task using Pydantic models for input validation and output formatting.

### Factory

Dria’s Factory offers various ready-to-use Singletons for different scenarios, easily compatible with a `DatasetGenerator` object. 
For more specific needs, however, creating your own Singleton is recommended.

Here's a basic example of how to use a singleton. Code below uses the `Simple` singleton from library which takes a prompt and executes it. 

```python
from dria import DriaDataset, DatasetGenerator, Model
from dria.factory import Simple
import asyncio

my_dataset = DriaDataset(
    name="simple",
    description="A simple dataset",
    schema=Simple.OutputSchema,
)
generator = DatasetGenerator(dataset=my_dataset)

instructions = [
    {
        "prompt": "Write a haiku about open source AI."
    },
]
asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=Simple,
        models=Model.LLAMA_3_1_8B_OR,
    )
)
my_dataset.to_json()

```

Output is:

```json
[
   {
      "prompt":"Write a haiku about open source AI.",
      "generation":"Code for all to see free\nSharing wisdom, knowledge flows\nHumanity's gift back",
      "model":"meta-llama\/llama-3.1-8b-instruct"
   }
]
```

## Writing Singletons

Dria's factory is limited, therefore writing a Singleton can adapt Dria Network to any problem at hand. 

### Basic Structure
A singleton consists of three main components:

1. Input fields (using Pydantic Fields)
2. Output schema (using Pydantic BaseModel)
3. Workflow and callback methods

We can start by importing the necessary libraries and defining the input fields and output schema.

```python
from dria.factory.utilities import get_abs_path
from dria.factory.workflows.template import SingletonTemplate
from dria.models import TaskResult
```

First step is to create a class that inherits from `SingletonTemplate` and define the input fields.

```python
class ValidatePrediction(SingletonTemplate):
    # Input fields
    prediction: str = Field(..., description="The predicted answer to be evaluated")
    correct_answer: str = Field(
        ..., description="The correct answer to compare against"
    )
```

`SingletonTemplate` is a base class that provides the necessary functionality to create pre-built tasks.
Next step is to create the output schema.

```python
class ValidationOutput(BaseModel):
    prediction: str = Field(..., description="The prediction result.")
    correct_answer: str = Field(..., description="The correct answer.")
    validation: bool = Field(..., description="Validation result (True/False)")
    model: str = Field(..., description="Model used for validation")
```

Output schema is attached to the singleton with built-in `OutputSchema` attribute. 

```python
class ValidatePrediction(SingletonTemplate):
    # Input fields
    prediction: str = Field(..., description="The predicted answer to be evaluated")
    correct_answer: str = Field(
        ..., description="The correct answer to compare against"
    )

    # Output schema
    OutputSchema = ValidationOutput
```

Singleton class has two abstrat methods that need to be implemented: `workflow` and `callback`.

```python
def workflow(self) -> Workflow
def callback(self, result: List[TaskResult]) -> List[ValidationOutput]
```

See [workflows]("how-to/workflows.md") for more information on how to implement workflows.

The `workflow` method defines the task to be executed and `callback` method processes the result.

```python
    def workflow(self) -> Workflow:
        """
        Generate a Task to determine if the predicted answer is contextually and semantically correct.

        Returns:
            Workflow: The constructed workflow
        """
        # Initialize the workflow with variables
        builder = WorkflowBuilder(
            prediction=self.prediction, correct_answer=self.correct_answer
        )

        # Add a generative step using the prompt
        builder.generative_step(
            path=get_abs_path("validate.md"),
            operator=Operator.GENERATION,
            outputs=[Write.new("validation_result")],
        )

        # Define the flow of the workflow
        flow = [Edge(source="0", target="_end")]
        builder.flow(flow)

        # Set the return value of the workflow
        builder.set_return_value("validation_result")
        return builder.build()
```

Since Dria supports multiple models, [structured outputs](../structured_outputs) are not forced. But can be added through `schema` field of `generative_step`. 
If not, the format and parsing is up to the prompt you provided to the task.

This is the implemented prompt for `Validator`

```markdown
You will be given a predicted answer to a question. Your task is to reason with your existing knowledge to evaluate if the predicted answer is correct or not.

Here is the predicted answer:
<prediction>
{{prediction}}
</prediction>

Here is the question answer:
<question>
{{correct_answer}}
</question>

To complete this task:
1. Carefully read both the prediction and the correct answer.
2. Compare the two answers, focusing on their semantic meaning and contextual relevance.
3. Determine if the predicted answer conveys the same core information and is contextually appropriate, even if the wording is different.
4. Ignore minor differences in phrasing, word choice, or additional details as long as the main point is correct.

Output your decision as follows:
- If the predicted answer is contextually and semantically correct, output only the word "true" (without quotes).
- If the predicted answer is not contextually or semantically correct, output only the word "false" (without quotes).

Do not provide any explanation or justification for your decision. Your entire response should consist of a single word: either "true" or "false".
```

Based on this prompt, we add a `callback` method:

```python
    def callback(self, result: List[TaskResult]) -> List[ValidationOutput]:
        """
        Parse the results into validated ValidationOutput objects

        Args:
            result: List of TaskResult objects

        Returns:
            List[ValidationOutput]: List of validated outputs
        """
        outputs = []
        for r in result:
            if r.result.lower() == "true":
                outputs.append(
                    ValidationOutput(
                        prediction=self.prediction,
                        correct_answer=self.correct_answer,
                        validation=True,
                        model=r.model,
                    )
                )
            elif r.result.lower() == "false":
                outputs.append(ValidationOutput(validation=False, model=r.model))
            else:
                raise ValueError("The result is not a boolean value.")
        return outputs
```