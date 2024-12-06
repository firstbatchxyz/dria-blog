# DriaDataset: The Core of Dria

The `DriaDataset` class serves as the foundation of Dria's data generation framework. 
It provides a structured way to create, manage, and persist data throughout the generation process.

1. Define a schema
2. Create a dataset (either empty or with existing data)

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

```python
from pydantic import BaseModel
from dria.db.database import DatasetDB

# Define your schema
class MySchema(BaseModel):
    text: str
    label: int

# Create dataset
dataset = DriaDataset(
    name="my_dataset",
    description="Example dataset",
    schema=MySchema,
    db=DatasetDB()
)
```

## Create From Existing

`DriaDataset` can be initialized with existing data. 

### From JSON
```python
dataset = DriaDataset.from_json(
    name="json_dataset",
    description="Dataset from JSON",
    schema=MySchema,
    db=db,
    json_path="data.json"
)
```

### From CSV
```python
dataset = DriaDataset.from_csv(
    name="csv_dataset",
    description="Dataset from CSV",
    schema=MySchema,
    db=db,
    csv_path="data.csv",
    delimiter=",",
    has_header=True
)
```

### From HuggingFace
```python
dataset = DriaDataset.from_huggingface(
    name="hf_dataset",
    description="Dataset from HuggingFace",
    schema=MySchema,
    db=db,
    dataset_id="username/dataset",
    mapping={"text": "input", "label": "class"}
)
```

## Schema Management

### Update Schema
```python
# Add new fields to schema
dataset.update_schema({"new_field": (str, ...)})
```

## Data Access

```python
# Get all entries
entries = dataset.get_entries()

# Get entries without metadata
data_only = dataset.get_entries(data_only=True)
```

## Key Features

1. **Schema Validation**: Ensures data consistency using Pydantic models
2. **Flexible Import/Export**: Supports multiple data formats
3. **Database Integration**: Persistent storage with DatasetDB
4. **Schema Evolution**: Ability to update schema and mutate data
5. **Training Format**: Specialized formatting for ML training
6. **Data Validation**: Automatic validation of entries against schema

## Notes

- Always initialize with a proper schema for data validation
- Use appropriate data types in schema definition
- Consider memory limitations when working with large datasets
- Ensure proper database configuration for persistence