---
categories:
- Applied AI
description: Explore methods for evaluating RAG systems using synthetic data to enhance
  question-answering applications performance.
tags:
- RAG Systems
- Synthetic Data
- AI Evaluation
- Question-Answering
- Deep Learning
---

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
class QuestionAnswer(BaseModel):
    question: str = Field(...)
    answer: List[Fact] = Field(...)

    @model_validator(mode="after")
    def validate_sources(self) -> "QuestionAnswer":
        self.answer = [fact for fact in self.answer if len(fact.substring_quote) > 0]
        return self
```

To implement the RAG pipeline, we'll use the `NaiveRAG` class:

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

def answer(self, query: str, context: str) -> QuestionAnswer:
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

We'll use the `QAPipeline` [class](../factory/qa.md) from `dria.factory` to generate question-answer pairs based on the document chunks.

#### The `QAPipeline` Class

Import the `QAPipeline` class from `dria.factory`:

```python
from dria.factory import QAPipeline
```

We define our *simulation* as:
> "People from different backgrounds trying to learn how to build an efficient RAG pipeline. Developers, developers in big corporations, businesses that try to implement RAG in to their custom docs, AI researchers."

Description of simulation determines the backstories for the generated questions.

Along with it, we specify the persona for the pipeline. 

> "A researcher that is concise and direct"

Persona determines how answers are generated based on the context provided.

We'll use existing chunks as our context to generate questions.

```python
file_chunks = ["\n".join(v) for k,v in chunker.get_files().items()]
```

Instead of using chunks directly, we are merging them as files, and using files as whole to boost pipelines ability to generate coherent questions.

```python
pipeline = QAPipeline(dria, config=PipelineConfig()).build(
    simulation_description="People from different backgrounds trying to learn how to build an efficient RAG pipeline. Developers, developers in big corporations, businesses that try to implement RAG in to their custom docs, AI researchers.",
    num_samples=2,
    persona="A researcher that is concise and direct",
    chunks=file_chunks
)
```

We can now execute the pipeline to generate question-answer pairs.

```python
async def run_pipeline(dria: Dria, chunker: ReadmeChunker):
    # read each chunk belonging to a file and merge them into a single string
    file_chunks = ["\n".join(v) for k,v in chunker.get_files().items()]
    print(f"num_files: {len(file_chunks)}")
    await dria.initialize()

    pipeline = QAPipeline(dria, config=PipelineConfig()).build(
        simulation_description="People from different backgrounds trying to learn how to build an efficient RAG pipeline. Developers, developers in big corporations, businesses that try to implement RAG in to their custom docs, AI researchers.",
        num_samples=2,
        persona="A researcher that is concise and direct",
        chunks=file_chunks
    )

    result = await pipeline.execute(return_output=True)
    with open("qa.json", "w") as f:
        json.dump(result, f, indent=4)
```

### Generating Multi-hop Questions

We'll use the `MultiHopQuestion` [class](../factory/multihopqa.md)  from `dria.factory` to generate multi-hop questions that require reasoning across multiple document chunks.

#### The `MultiHopQuestion` Class

Unlike simple QA pairs, multi-hop questions require reasoning across multiple document chunks.
`MultiHopQuestion` class is a Singleton, not a pipeline. It's a single atomic task so we'll use it with our `ParallelSingletonExecutor`.

Import the `MultiHopQuestion` class from `dria.factory`:

```python
from dria.factory import MultiHopQuestion
```

We'll initialize selected singleton and pass it to the `ParallelSingletonExecutor` for execution.

```python
singleton = MultiHopQuestion()
executor = ParallelSingletonExecutor(dria, singleton)
```

We set the model pools for the executor
```python
executor.set_models([Model.GPT4O, Model.GEMINI_15_FLASH, Model.QWEN2_5_32B_FP16, Model.GEMINI_15_FLASH])
```

Then load the instructions for the executor. We'll randomly sample 3 chunks from each file to create multi-hop questions.

```python
executor.load_instructions([{"chunks": random.sample(file_chunks, 3)} for _ in range(20)])
```

Here is the complete code to generate multi-hop questions:

```python
async def run_multihop_tasks(dria: Dria, chunker: ReadmeChunker):
    file_chunks = ["\n".join(v) for k, v in chunker.get_files().items()]
    singleton = MultiHopQuestion()
    executor = ParallelSingletonExecutor(dria, singleton)
    # Set model pools
    executor.set_models([Model.GPT4O, Model.GEMINI_15_FLASH, Model.QWEN2_5_32B_FP16, Model.GEMINI_15_FLASH])
    executor.load_instructions([{"chunks": random.sample(file_chunks, 3)} for _ in range(20)])
    results = await executor.run()
    with open("multihop_output.json", "w") as f:
        json.dump(results, f, indent=4)
```

That's it for generating synthetic data for evaluation.


## Evaluation

To evaluate the RAG pipeline, we need to compare the generated questions and answers with the ground truth.

### Evaluator Class
The `Evaluator` class uses the `instructor` library to interact with OpenAI's API for chat completions to evaluate the generated questions.

We'll use the `EvaluationResult` pydantic model to structure the data for validation and processing.

```python
class EvaluationResult(BaseModel):
    evaluation: str = Field(...)
    reasoning: str = Field(...)


class Evaluator:
    def __init__(self):
        self.client = instructor.from_openai(OpenAI())

    def evaluate(self, question: str, context: str, prediction: str, ground_truth: str) -> EvaluationResult:

      return self.client.chat.completions.create(
          model="gpt-4o-mini",
          temperature=0,
          response_model=EvaluationResult,
          messages=[
              {
                  "role": "system",
                  "content": "You are a world class algorithm to evaluate predicted questions.",
              },
              {"role": "user", "content": f"{context}"},
              {"role": "user", "content": f"Question: {question}"},
              {"role": "user", "content": f"Prediction: {prediction}"},
              {"role": "user", "content": f"Ground truth: {ground_truth}"},
          ]
      )
```

### Evaluating the Pipeline

We can now evaluate the generated questions and answers using the `Evaluator` class.

```python
answers = []
evaluate = Evaluator()

# Load QA data
with open("qa.json", "r") as f:
    qa = json.loads(f.read())

# Load MultiHop QA
with open("multihop_output.json", "r") as f:
    multi_hop_qa = json.loads(f.read())

# Process simple QA
for pair in tqdm(qa):
    docs = rag.search(pair["question"])
    answer = rag.answer(pair["question"], "\n".join(docs))
    answers.append({
        "prediction": answer,
        "answer": pair["answer"],
        "type": "simple",
        "question": pair["question"],
        "context": "\n".join(docs)
    })

# Process multi-hop QA
for pair in tqdm(multi_hop_qa):
    for hop_type in ["1-hop", "2-hop", "3-hop"]:
        docs = rag.search(pair[hop_type])
        answer = rag.answer(pair[hop_type], "\n".join(docs))
        answers.append({
            "prediction": answer,
            "answer": pair["answer"],
            "type": hop_type,
            "question": pair[hop_type],
            "context": "\n".join(docs)
        })

# Evaluate all answers
evaluated_answers = []
for answer in tqdm(answers):
    result = evaluate.evaluate(answer["question"], answer["context"], answer["prediction"], answer["answer"])
    evaluated_answers.append({"question": answer["question"], "answer": answer["answer"],
                              "prediction": "\n".join([f.fact for f in answer["prediction"].answer]),
                              "evaluation": result.evaluation.lower(), "reasoning": result.reasoning})
```


*Expected output*

```commandline
100%|██████████| 209/209 [13:29<00:00,  3.87s/it]
100%|██████████| 19/19 [02:13<00:00,  7.00s/it]
Total evaluations: 266
Correct: 56 (21.05%)
Partially Correct: 107 (40.23%)
Incorrect: 42 (15.79%)
```

There you have it! 

A complete guide to evaluating RAG systems with synthetic data. 
Please note we're using NaiveRAG and synthetic data for demonstration purposes. 
Different RAG implementations and real-world data may yield different results.

## Code

Complete script for the RAG pipeline can be found in [SDK](https://github.com/firstbatchxyz/dria-sdk/tree/master/examples/rag_evaluation) examples.