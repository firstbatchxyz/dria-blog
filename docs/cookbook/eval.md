# Evaluating RAG Systems with Synthetic Data 

Retrieval-Augmented Generation systems are powerful tools for building AI-powered question-answering applications. 
Creating a diverse dataset of question & answer pairs that includes complex queries will help you quickly evaluate your RAG pipeline and generate metrics.

Evaluation is crucial to understanding the performance of your RAG system and identifying areas for improvement. There are multiple parameters to consider when evaluating a RAG system, including but not limited to:

- Embedding model choice
- Retrieval method (BM25, VectorDB, hybrid)
- Reranking strategy
- Answer generation model
- Chunking strategy

Synthetic baseline data can help you evaluate your RAG system's performance across these parameters.
For instance, you can try different embedding models and evaluate their impact on the system's performance.

This guide demonstrates how to evaluate RAG systems using synthetic data, providing a practical approach to testing and improving your implementation. 

If you are in a hurry, you can jump straight to the [code implementation](#code).

## Table of Contents
- [Setting up a the RAG pipeline](#setup)
- [Generating Synthetic Data](#generating-synthetic-data)
- [Evaluating RAG](#evaluation)

## Setup 

Before getting started, ensure you have Python 3.10 or later installed. 

Set up your environment using conda: 
```bash 
conda create -n rag python=3.10 conda activate rag 
``` 

Install the required dependencies: 
```bash 
pip install -U langchain-core langchain-openai langchain_community instructor dria 
``` 

### Document Chunking 

For this cookbook, we'll work with Jason Liu's [blog](https://jxnl.co/) repository. Clone the repository to project root directory.

```commandline
git clone https://github.com/jxnl/blog/
```

Repository by `jxnl` consists of multiple markdown files. 

First, we'll create a `ReadmeChunker` class to process markdown documents into manageable chunks: 

```python
class ReadmeChunker:
    def __init__(self, docs_dir: str, min_chunk_size: int = 500):
        self.docs_dir = Path(docs_dir)
        self.min_chunk_size = min_chunk_size
        self.chunks = self._process_markdown_files()
```

We'll chunk these files using `#` header tags to create meaningful chunks for our RAG pipeline. 
Check full implementation [here](#code).


```python
def _chunk_by_headers(self, markdown_text: str) -> List[str]:
    """
    Split markdown text into chunks based on headers.

    Args:
        markdown_text (str): The markdown text to chunk

    Returns:
        List[str]: List of text chunks
    """
    header_pattern = r'^#{1,6}\s.*$'
    chunks = []
    current_chunk = []
    current_size = 0

    for line in markdown_text.split('\n'):
        if (re.match(header_pattern, line) and
            current_size > self.min_chunk_size):
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = len(line)
        else:
            current_chunk.append(line)
            current_size += len(line) + 1

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks
```

The `ReadmeChunker` class handles:

- Processing markdown files from a specified directory
- Splitting content into chunks based on headers
- Maintaining minimum chunk sizes for optimal processing


### *Creating a VectorDB*

Next, we implement the vector store for efficient document retrieval using `InMemoryVectorStore` from `langchain_core.vectorstores`. 
It's an in-memory implementation of VectorStore using a dictionary. Uses numpy to compute cosine similarity for search. 
We'll use OpenAI's embeddings for our case. 


```python
class VectorStore:
    def __init__(self, embedding_model: Optional[Any] = None):
        self.embedding_model = embedding_model or OpenAIEmbeddings()
        self.vector_store = InMemoryVectorStore(self.embedding_model)
```

Add documents with metadata to the vector store along with search:

```python
    def add_documents(self, documents: List[Document]) -> None:
          self.vector_store.add_documents(documents)
    
    def search(self, query: str, top_k=3):
        return self.vector_store.similarity_search(
                    query=query,
                    k=top_k
                )
```

That's it! VectorDB is ready for use in our RAG pipeline.

### RAG Implementation

RAG is implemented in the `NaiveRAG` class using both the `ReadmeChunker` and `VectorStore` classes.
We'll use the `instructor` library to interact with OpenAI's API for chat completions for structured outputs.

Code taken from Instructor's [cookbook](https://python.useinstructor.com/examples/exact_citations/#validation-method-validate_sources).
Pydantic classes structures the responses returned from `OpenAI` API. 

*From the blog*:

_This example shows how to use Instructor with validators to not only add citations to answers generated but also prevent hallucinations by ensuring that every statement made by the LLM is backed up by a direct quote from the context provided, and that those quotes exist!
Two Python classes, Fact and QuestionAnswer, are defined to encapsulate the information of individual facts and the entire answer, respectively._


#### The `Fact` Class
The Fact class encapsulates a single statement or fact. It contains two fields:

- `fact`: A string representing the body of the fact or statement.
- `substring_quote`: A list of strings. Each string is a direct quote from the context that supports the fact.


#### The `QuestionAnswer` Class
This class encapsulates the question and its corresponding answer. It contains two fields:

- `question`: The question asked.
- `answer`: A list of Fact objects that make up the answer.


```python
from pydantic import BaseModel, Field, model_validator, ValidationInfo
from typing import List
import re

class Fact(BaseModel):
    fact: str = Field(...)
    substring_quote: List[str] = Field(...)

    @model_validator(mode="after")
    def validate_sources(self, info: ValidationInfo) -> "Fact":
        text_chunks = info.context.get("text_chunk", None)
        spans = list(self.get_spans(text_chunks))
        self.substring_quote = [text_chunks[span[0] : span[1]] for span in spans]
        return self

    def get_spans(self, context):
        for quote in self.substring_quote:
            yield from self._get_span(quote, context)

    def _get_span(self, quote, context):
        for match in re.finditer(re.escape(quote), context):
            yield match.span()

class QuestionAnswer(BaseModel):
    question: str = Field(...)
    answer: List[Fact] = Field(...)

    @model_validator(mode="after")
    def validate_sources(self) -> "QuestionAnswer":
        self.answer = [fact for fact in self.answer if len(fact.substring_quote) > 0]
        return self
```

To implement the RAG pipeline, we'll use the `MiniRAG` class:

#### The `NaiveRAG` Class

- `chunker`: ReadmeChunker instance to process markdown files.
- `vectorstore`: VectorStore instance to manage vector storage and similarity search operations.
- `client`: Instructor client to interact with OpenAI's API.


```python
import instructor
from langchain_core.documents import Document
from openai import OpenAI

class NaiveRAG:
    def __init__(self):
        self.chunker = ReadmeChunker("blog/docs")
        self.vectorstore = VectorStore()
        self.vectorstore.add_documents([Document(id=str(i), page_content=chunk["chunk"], metadata={"path": chunk["path"]}) for i, chunk in enumerate(chunker.get_chunks())])
        self.client = instructor.from_openai(OpenAI())
```

Now we need `search` and `answer` methods to complete RAG pipeline.

- `search`: Retrieve relevant documents based on the query.
- `answer`: Generate a response using the retrieved documents.

We'll use `QuestionAnswer` pydantic model to structure the data for validation and processing.

```python
def search(self, query: str, top_k=3):
    results = self.vectorstore.similarity_search(query=query, k=top_k)
    return [doc.page_content for doc in results]

def answer(self, query: str) -> QuestionAnswer:
  context = "\n".join(self.search(query))
  return self.client.chat.completions.create(
      model="gpt-4o-mini",
      temperature=0,
      response_model=QuestionAnswer,
      messages=[
          {
              "role": "system",
              "content": "You are a world class algorithm to answer questions with correct and exact citations.",
          },
          {"role": "user", "content": f"{context}"},
          {"role": "user", "content": f"Question: {query}"},
      ],
      validation_context={"text_chunk": context},
  )
```

And that's it! We have a complete RAG pipeline ready for evaluation.

---

## Generating Synthetic Data

To evaluate the RAG pipeline, we need a diverse dataset of question-answer pairs based on the document chunks we processed earlier.
Our objective is to generate two datasets:

1. **Questions**: A set of questions based on the document chunks and different personas. 
2. **Multi-hop Questions**: A set of multi-hop questions that require reasoning across multiple document chunks.

### Generating QA Pairs

We'll use the `QAPipeline` [class]((factory/qa.md)) from `dria.factory` to generate question-answer pairs based on the document chunks.

#### The `QAPipeline` Class


```python
pipeline = QAPipeline(dria, config=PipelineConfig()).build(
    simulation_description="People from different background trying learn how to build an efficient RAG pipeline. Developers, developers in big corporations, bussiness that try to inplement RAG in to their custom docs, AI researchers.",
    num_samples=2,
    persona="A researcher that is concise and direct",
    chunks=file_chunks
)
```

```python
import os
from dria.client import Dria
from dria.pipelines import PipelineConfig
from dria.factory import QAPipeline
import asyncio
import json


dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])

async def run_pipeline():
    # read each chunk belonging to a file and merge them into a single string
    file_chunks = ["\n".join(v) for k,v in get_files().items()]
    print(f"num_files: {len(file_chunks)}")
    await dria.initialize()

    pipeline = QAPipeline(dria, config=PipelineConfig()).build(
        simulation_description="People from different background trying learn how to build an efficient RAG pipeline. Developers, developers in big corporations, bussiness that try to inplement RAG in to their custom docs, AI researchers.",
        num_samples=2,
        persona="A researcher that is concise and direct",
        chunks=file_chunks
    )

    result = await pipeline.execute(return_output=True)
    with open("qa.json", "w") as f:
        json.dump(result, f, indent=4)



loop = asyncio.get_running_loop()
await loop.create_task(run_pipeline())
```

## Code

Entire script for the RAG pipeline:

[Notebook]()

```python

from typing import List, Optional, Dict, Any
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from pydantic import BaseModel, Field, model_validator, ValidationInfo
from openai import OpenAI
import instructor
from pathlib import Path
import re
import os
from collections import defaultdict
from dria.client import Dria
from dria.factory import QAPipeline
from dria.pipelines import PipelineConfig
import asyncio
import json

class ReadmeChunker:
    """A class to chunk markdown files based on headers."""

    def __init__(self, docs_dir: str, min_chunk_size: int = 500):
        """
        Initialize the ReadmeChunker.

        Args:
            docs_dir (str): Directory containing markdown files
            min_chunk_size (int): Minimum size of chunks in characters
        """
        self.docs_dir = Path(docs_dir)
        self.min_chunk_size = min_chunk_size
        self.chunks = self._process_markdown_files()

    def _process_markdown_files(self) -> List[dict]:
        """Process all markdown files in the directory."""
        all_chunks = []

        try:
            for file_path in self.docs_dir.rglob("*.md"):
                chunks = self._process_single_file(file_path)
                all_chunks.extend(chunks)

            return all_chunks

        except Exception as e:
            raise Exception(f"Error processing markdown files: {str(e)}")

    def _process_single_file(self, file_path: Path) -> List[dict]:
        """
        Process a single markdown file.

        Args:
            file_path (Path): Path to the markdown file

        Returns:
            List[str]: List of chunks from the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return [{"chunk":ch, "path":file_path} for ch in self._chunk_by_headers(content)]

        except Exception as e:
            print(f"Warning: Could not process {file_path}: {str(e)}")
            return []

    def _chunk_by_headers(self, markdown_text: str) -> List[str]:
        """
        Split markdown text into chunks based on headers.

        Args:
            markdown_text (str): The markdown text to chunk

        Returns:
            List[str]: List of text chunks
        """
        header_pattern = r'^#{1,6}\s.*$'
        chunks = []
        current_chunk = []
        current_size = 0

        for line in markdown_text.split('\n'):
            if (re.match(header_pattern, line) and
                current_size > self.min_chunk_size):
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = len(line)
            else:
                current_chunk.append(line)
                current_size += len(line) + 1

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks
    def get_chunks(self):
      return self.chunks
    
    def get_files(self):
      chunks = self.get_chunks()
      files = defaultdict(list)
      for chunk in chunks:
        files[str(chunk["path"])].append(chunk["chunk"])
      return files

class VectorStore:
    """A class to manage vector storage and similarity search operations."""

    def __init__(self, embedding_model: Optional[Any] = None):
        """
        Initialize the VectorStore.

        Args:
            embedding_model: The embedding model to use (defaults to OpenAIEmbeddings)
        """
        self.embedding_model = embedding_model or OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
        self.vector_store = InMemoryVectorStore(self.embedding_model)

    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.

        Args:
            documents (List[Document]): List of Document objects to add
        """
        try:
              self.vector_store.add_documents(documents)
        except Exception as e:
            raise Exception(f"Error adding documents to vector store: {str(e)}")

    def similarity_search(self,
                         query: str,
                         k: int = 1,
                         filter: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        Perform similarity search on the vector store.

        Args:
            query (str): The search query
            k (int): Number of results to return
            filter (Dict): Optional metadata filter

        Returns:
            List[Document]: List of similar documents
        """
        if self.vector_store is None:
            raise ValueError("Vector store is empty. Add documents first.")

        try:
            if filter:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter=filter
                )
            else:
                results = self.vector_store.similarity_search(
                    query=query,
                    k=k
                )
            return results

        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")

# https://python.useinstructor.com/examples/exact_citations/#validation-method-validate_sources

class Fact(BaseModel):
    fact: str = Field(...)
    substring_quote: List[str] = Field(...)

    @model_validator(mode="after")
    def validate_sources(self, info: ValidationInfo) -> "Fact":
        text_chunks = info.context.get("text_chunk", None)
        spans = list(self.get_spans(text_chunks))
        self.substring_quote = [text_chunks[span[0] : span[1]] for span in spans]
        return self

    def get_spans(self, context):
        for quote in self.substring_quote:
            yield from self._get_span(quote, context)

    def _get_span(self, quote, context):
        for match in re.finditer(re.escape(quote), context):
            yield match.span()

class QuestionAnswer(BaseModel):
    question: str = Field(...)
    answer: List[Fact] = Field(...)

    @model_validator(mode="after")
    def validate_sources(self) -> "QuestionAnswer":
        self.answer = [fact for fact in self.answer if len(fact.substring_quote) > 0]
        return self

class NaiveRAG:
    def __init__(self):
        
        self.chunker = ReadmeChunker("blog/docs")
        self.vectorstore = VectorStore()
        self.vectorstore.add_documents([Document(id=str(i), page_content=chunk["chunk"], metadata={"path": chunk["path"]}) for i, chunk in enumerate(self.chunker.get_chunks())])
        self.client = instructor.from_openai(OpenAI())

    def search(self, query: str, top_k=3):
        results = self.vectorstore.similarity_search(query=query, k=top_k)
        return [doc.page_content for doc in results]

    def answer(self, query: str) -> QuestionAnswer:
      context = "\n".join(self.search(query))
      return self.client.chat.completions.create(
          model="gpt-4o-mini",
          temperature=0,
          response_model=QuestionAnswer,
          messages=[
              {
                  "role": "system",
                  "content": "You are a world class algorithm to answer questions with correct and exact citations.",
              },
              {"role": "user", "content": f"{context}"},
              {"role": "user", "content": f"Question: {query}"},
          ],
          validation_context={"text_chunk": context},
      )

async def run_pipeline(dria: Dria, chunker: ReadmeChunker):
    # read each chunk belonging to a file and merge them into a single string
    file_chunks = ["\n".join(v) for k,v in chunker.get_files().items()]
    print(f"num_files: {len(file_chunks)}")
    await dria.initialize()

    pipeline = QAPipeline(dria, config=PipelineConfig()).build(
        simulation_description="People from different background trying learn how to build an efficient RAG pipeline. Developers, developers in big corporations, bussiness that try to inplement RAG in to their custom docs, AI researchers.",
        num_samples=2,
        persona="A researcher that is concise and direct",
        chunks=file_chunks
    )

    result = await pipeline.execute(return_output=True)
    with open("qa.json", "w") as f:
        json.dump(result, f, indent=4)



loop = asyncio.get_running_loop()
await loop.create_task(run_pipeline())

```