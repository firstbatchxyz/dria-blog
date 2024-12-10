---
categories:
- Workflows
description: Learn about structured outputs and how to implement them in Dria Network
  with examples and JSON Schema.
tags:
- Structured Outputs
- Dria Network
- JSON Schema
- OpenAI
- Workflows
---

# Structured Outputs

Structured outputs best explained in OpenAI's [blog post](https://platform.openai.com/docs/guides/structured-outputs):

> Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema, so you don't need to worry about the model omitting a required key, or hallucinating an invalid enum value. 


Dria Network supports structured outputs for providers including `OpenAI`, `Gemini` and `Ollama`.
However, structured outputs are only supported by models that are capable of [function](functions.md) calling. 

Enabling structured outputs is simple. You just need to provide a schema to the `WorkflowBuilder` instance, rest will be handled by Dria SDK.

From the previous example in [singleton](singletons.md), you can directly attach the OutputSchema to your workflow for structured output.

```python
 builder.generative_step(
        path=get_abs_path("validate.md"),
        operator=Operator.GENERATION,
        schema=self.OutputSchema,
        outputs=[Write.new("validation_result")],
    )
```

Full workflow method:

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
            schema=self.OutputSchema,
            outputs=[Write.new("validation_result")],
        )

        # Define the flow of the workflow
        flow = [Edge(source="0", target="_end")]
        builder.flow(flow)

        # Set the return value of the workflow
        builder.set_return_value("validation_result")
        return builder.build()
```