# Singletons

Singletons are pre-built task templates that perform specific functions using a standardized structure. 
Each singleton is designed as a single instance that handles a specific task using Pydantic models for input validation and output formatting.
### Factory

Dria’s Factory offers various ready-to-use Singletons for different scenarios, easily compatible with a DatasetGenerator object. 
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
