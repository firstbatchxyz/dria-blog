---
categories:
- Data Generation
description: CSVExtenderPipeline class extends CSV data by generating new rows based
  on existing entries, enhancing data analysis and organization.
tags:
- CSV
- Data Processing
- Data Extension
- Pipeline
- Automation
---

# CSVExtenderPipeline

`CSVExtenderPipeline` is a class that creates a pipeline for extending a given `csv`. The pipeline generates new rows based on the existing ones.

## Overview

This pipeline extends a given `csv` by generating new rows based on the existing ones. The extension is done by adding new subcategories to the existing categories. The number of subcategories can be specified to determine the number of rows to be generated.

#### Input

- `csv` (`str`): The csv data to be extended.
- `num_values` (`int`): The number of new independent values
- `num_rows` (`int`): The number of rows to be generated for each value

> You'll get num_values * num_rows new entries in the output.

#### Expected output (probably a large file)

```json
{
  "extended_csv": "category,subcategory,task\nFile System, File, Create a new File\nFile System, File, Edit the contents of a File\nFile System, File, Read the contents of a File\nFile System, File, Delete a File\nFile System, File, Copy a File\nFile System, File, Move a File\nFile System, File, Rename a File\nFile Syste, Folder, Create a new Folder\nFile System, Folder, Delete a Folder\nFile System, Folder, Copy a Folder\nFile System, Folder, Move a Folder\nFile System, Folder, Rename a Folder\nFile System, Folder, List the contents of a Folder\nFile System, Folder, Move a File to a Folder\nFile System, Folder, Copy a File to a Folder\nWeb Browser, Search, Search over a query\nWeb Browser, Search, Search for images\nWeb Browser, Search, Search for news\nWeb Browser, Access, Scrape the content of a website\nWeb Browser, Access, Take a screenshot of a website\nWeb Browser, Access, Download a file/files from a website\nWeb Browser, Access, Fill out forms\nCommunication, Email, Send an email\nCommunication, Email, Read the contents of an email\nCommunication, Email, Retrieve the last n emails\nScheduling, To-Do List"
} 
```