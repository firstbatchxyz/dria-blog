---
categories:
- Data Generation
description: CSVExtenderPipeline class allows easy extension of CSV files by generating
  new rows from existing data with specified subcategories.
tags:
- CSV
- Data Processing
- Pipeline
- Async Programming
- Data Generation
---

# CSVExtenderPipeline

`CSVExtenderPipeline` is a class that creates a pipeline for extending a given `csv`. The pipeline generates new rows based on the existing ones.

## Overview

This pipeline extends a given `csv` by generating new rows based on the existing ones. The extension is done by adding new subcategories to the existing categories. The number of subcategories can be specified to determine the number of rows to be generated.

#### Input

- `csv` (`str`): The csv data to be extended.
- `num_values` (`int`): The number of columns for extended csv.
- `num_rows` (`int`): The number of rows for extended csv.

```python
import asyncio
import os

from dria.client import Dria
from dria.factory import CSVExtenderPipeline
from dria.pipelines import PipelineConfig
import json

dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])

# Your csv as string
data = """category,subcategory,task
File System, File, Create a new File
File System, File, Edit the contents of a File
File System, File, Read the contents of a File
File System, File, Delete a File
File System, File, Copy a File
File System, File, Move a File
File System, File, Rename a File"""


async def evaluate():
    await dria.initialize()
    pipeline = CSVExtenderPipeline(dria, PipelineConfig()).build(csv=data, num_values=10, num_rows=10)
    res = await pipeline.execute(return_output=True)
    print("Done")
    with open("csv.json", "w") as f:
        f.write(json.dumps(res, indent=2))
    print(res)

if __name__ == "__main__":
    asyncio.run(evaluate())
```

Expected output (probably a large file)

```json
{
  "extended_csv": "category,subcategory,task\nFile System, File, Create a new File\nFile System, File, Edit the contents of a File\nFile System, File, Read the contents of a File\nFile System, File, Delete a File\nFile System, File, Copy a File\nFile System, File, Move a File\nFile System, File, Rename a File\nFile Syste, Folder, Create a new Folder\nFile System, Folder, Delete a Folder\nFile System, Folder, Copy a Folder\nFile System, Folder, Move a Folder\nFile System, Folder, Rename a Folder\nFile System, Folder, List the contents of a Folder\nFile System, Folder, Move a File to a Folder\nFile System, Folder, Copy a File to a Folder\nWeb Browser, Search, Search over a query\nWeb Browser, Search, Search for images\nWeb Browser, Search, Search for news\nWeb Browser, Access, Scrape the content of a website\nWeb Browser, Access, Take a screenshot of a website\nWeb Browser, Access, Download a file/files from a website\nWeb Browser, Access, Fill out forms\nCommunication, Email, Send an email\nCommunication, Email, Read the contents of an email\nCommunication, Email, Retrieve the last n emails\nScheduling, To-Do List"
} 
```
