---
categories:
- Data Generation
description: Explore the Dria Dataset class for efficient data generation, management,
  and persistence in Python projects.
tags:
- DriaDataset
- Data Generation
- Python
- Data Management
- Pydantic
---

# Dria Dataset

The `DriaDataset` class serves as the foundation of Dria's data generation framework. 
It provides a structured way to create, manage, and persist data throughout the generation process.

### Data Persistence
- All generated data is automatically saved to the dataset
- Intermediate steps in multi-stage generation processes are preserved
- Failed generation attempts are tracked and stored

### Flexible Initialization
- Start with an empty dataset
- Initialize with existing data (e.g., from Hugging Face datasets)
- Augment existing data or use existing data as instructions

### Data Management
- Schema validation ensures data consistency
- Multiple import/export options for compatibility
- Structured handling of complex datasets

## Basic Usage

Dria SDK operates through `DriaDataset`. 

Import packages
```python
from pydantic import BaseModel
from dria import DriaDataset
```

Define a pydantic schema

```python
# Define your schema
class MySchema(BaseModel):
    text: str
    label: int
```

Create a `DriaDataset`

```python
# Create dataset
dataset = DriaDataset(
    name="my_dataset",
    description="Example dataset",
    schema=MySchema,
)
```

## Create From Existing

`DriaDataset` can be initialized with existing data. 

### From HuggingFace

Create dataset by:

```python
from dria import DriaDataset
from pydantic import BaseModel, Field
from typing import List

class ConversationItem(BaseModel):
    from_: str = Field(..., alias="from")
    value: str

class ConversationData(BaseModel):
    conversations: List[ConversationItem]
    
my_dataset = DriaDataset.from_huggingface(name="subquery_data", description="A list of query and subqueries", dataset_id="andthattoo/subqueries", schema=ConversationData)
```

Reload data by using the same name and schema :
```python
class ConversationItem(BaseModel):
    from_: str = Field(..., alias="from")
    value: str

class ConversationData(BaseModel):
    conversations: List[ConversationItem]

my_dataset = DriaDataset(name="subquery_data", description="A list of query and subqueries", schema=ConversationData)
```

### From JSON & CSV

Same method applies for JSON and CSV files.

For JSON:

```python
dataset = DriaDataset.from_json(
    name="json_dataset",
    description="Dataset from JSON",
    schema=MySchema,
    json_path="data.json"
)
```

For CSV files:

```python
dataset = DriaDataset.from_csv(
    name="csv_dataset",
    description="Dataset from CSV",
    schema=MySchema,
    csv_path="data.csv",
    delimiter=",",
    has_header=True
)
```