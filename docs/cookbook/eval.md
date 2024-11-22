---
categories:
- RAG
description: Learn how to evaluate Retrieval-Augmented Generation (RAG) systems using
  synthetic data for improved performance and metrics.
tags:
- RAG
- Synthetic Data
- AI Evaluation
- Question Answering
- Data Generation
---

# Evaluating RAG Systems with Synthetic Data 

Retrieval-Augmented Generation systems are powerful tools for building AI-powered question-answering applications. 
Creating a diverse dataset of question & answer pairs that includes complex queries will help you quickly evaluate your RAG pipeline and generate metrics.

Evaluation is crucial to understanding the performance of your RAG system and identifying areas for improvement. 
There are multiple parameters to consider when evaluating a RAG system, including but not limited to:

- Embedding model choice
- Retrieval method (BM25, VectorDB, hybrid)
- Reranking strategy
- Answer generation model
- Chunking strategy

Synthetic baseline data can help you evaluate your RAG system's performance across these parameters.

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
pip install -U RAGatouille instructor dria datasets
``` 

#### For this cookbook, we'll work with HuggingFace [Docs](https://huggingface.co/datasets/m-ric/huggingface_doc) as our RAG dataset.


### RAG Implementation

RAG is implemented in the `RAG` class using [RAGatouille](https://github.com/AnswerDotAI/RAGatouille) as the backbone for retrieval, a library focuses on making ColBERT simple to use for developers.

We'll use the `instructor` library to interact with OpenAI's API for chat completions for structured outputs.

Code taken from Instructor's [cookbook](https://python.useinstructor.com/examples/exact_citations/#validation-method-validate_sources).
Pydantic classes structures the responses returned from `OpenAI` API. 

To implement the RAG pipeline, we'll use the `RAG` class:

#### The `RAG` Class

- `rag`: RAGPretrainedModel for ColBERT based retrieval.
- `client`: Instructor client to interact with OpenAI's API.


```python
import instructor
from ragatouille import RAGPretrainedModel
from openai import OpenAI

class RAG:
    def __init__(self, chunks):
        self.rag = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
        self.index_path = self.rag.index(index_name="my_index", collection=chunks)
        self.client = instructor.from_openai(OpenAI())
```

Now we need `search` and `answer` methods to complete RAG pipeline.

- `search`: Retrieve relevant documents based on the query.
- `answer`: Generate a response using the retrieved documents.

We'll use `QuestionAnswer` pydantic model to structure the data for validation and processing.

```python
    def search(self, question: str, top_k=3) -> Union[List[List[str]], List[str]]:
        res = self.rag.search(question, k=top_k)
        return [r["content"] for r in res]

    def answer(self, question: str) -> QuestionAnswer:

        docs = self.search(question)
        context = "\n".join(docs)

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
                {"role": "user", "content": f"Question: {question}"},
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
> AI developers and researchers learning Huggingface. Some focus on fine-tuning and post-training, others on RAG systems, retrieval problems, image models, or dataset work.

Description of simulation determines the backstories for the generated questions.

Along with it, we specify the persona for the pipeline. 

> A researcher that is concise and direct

Persona determines how answers are generated based on the context provided.

We'll use existing chunks as our context to generate questions.

Instead of using chunks directly, we are merging them as files, and using files as whole to boost pipelines ability to generate coherent questions.

```python
pipeline = QAPipeline(dria, config=PipelineConfig()).build(
    simulation_description="AI developers and researchers learning Huggingface. "
                           "Some focus on fine-tuning and post-training, others on RAG systems, "
                           "retrieval problems, image models, or dataset work.",
    num_samples=1,
    persona="A HuggingFace expert that is concise and direct",
    chunks=file_chunks,
)
```

We can now execute the pipeline to generate question-answer pairs.

```python
async def run_qa_pipeline(dria: Dria, file_chunks):
    await dria.initialize()

    pipeline = QAPipeline(dria, config=PipelineConfig()).build(
        simulation_description="AI developers and researchers learning Huggingface. "
                               "Some focus on fine-tuning and post-training, others on RAG systems, "
                               "retrieval problems, image models, or dataset work.",
        num_samples=1,
        persona="A HuggingFace expert that is concise and direct",
        chunks=file_chunks,
    )

    return await pipeline.execute(return_output=True)
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

We set the model pools for the executor, publishing tasks to nodes that work with the specified models. 
```python
executor.set_models([Model.GPT4O, Model.GEMINI_15_FLASH, Model.QWEN2_5_32B_FP16, Model.GEMINI_15_FLASH])
```

Then load the instructions for the executor. We'll randomly sample 3 chunks from each file to create multi-hop questions.

```python
executor.load_instructions([{"chunks": random.sample(file_chunks, 3)} for _ in range(10)])
```

Here is the complete code to generate multi-hop questions:

```python
async def run_multihop_tasks(dria: Dria, file_chunks):
    singleton = MultiHopQuestion()
    executor = ParallelSingletonExecutor(dria, singleton)
    executor.set_timeout(150)
    executor.set_models(
        [
            Model.QWEN2_5_72B_OR,
            Model.GEMINI_15_PRO,
            Model.GPT4O,
            Model.ANTHROPIC_SONNET_3_5_OR,
            Model.ANTHROPIC_HAIKU_3_5_OR,
        ]
    )
    executor.load_instructions(
        [{"chunks": random.sample(file_chunks, 3)} for _ in range(10)]
    )
    return await executor.run()
```

That's it for generating synthetic data for evaluation.


## Evaluation

To evaluate the RAG pipeline, we need to compare the generated questions and answers with the ground truth.

### Evaluator Class
The `Evaluator` class uses the `instructor` library to interact with OpenAI's API for chat completions to evaluate the generated questions.

We'll use the `EvaluationResult` pydantic model to structure the data for validation and processing.

```python
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI


class EvaluationResult(BaseModel):
    evaluation: str = Field(...)
    reasoning: str = Field(...)


class Evaluator:
    def __init__(self):
        self.client = instructor.from_openai(OpenAI())

    def evaluate(
        self, question: str, prediction: str, ground_truth: str
    ) -> EvaluationResult:

        return self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            response_model=EvaluationResult,
            messages=[
                {
                    "role": "system",
                    "content": "You are a world class judge to evaluate predicted answers to given question.",
                },
                {"role": "user", "content": f"Question: {question}"},
                {"role": "user", "content": f"Prediction: {prediction}"},
                {"role": "user", "content": f"Ground truth: {ground_truth}"},
            ],
        )

```

### Running the Evaluation pipeline

We can now evaluate the generated questions and answers using the `Evaluator` class.

```python
def main():

    # Load dataset
    dataset = load_dataset("m-ric/huggingface_doc")
    eval_chunks = dataset["train"].select(range(int(0.02 * len(dataset["train"]))))
    eval_chunks = [chunk["text"] for chunk in eval_chunks]

    # Create synthetic evaluation data using %2 of the dataset
    dria = Dria(rpc_token=os.environ["DRIA_RPC_TOKEN"])
    qa_eval = asyncio.run(run_qa_pipeline(dria, eval_chunks))
    multihop_eval = asyncio.run(run_multihop_tasks(dria, eval_chunks))

    # Initialize RAG
    all_chunks = dataset["train"]
    all_chunks = [chunk["text"] for chunk in all_chunks]
    rag = RAG(all_chunks)

    answers = []
    evaluate = Evaluator()

    # Answer QA data
    for pair in tqdm(qa_eval):
        answer = rag.answer(pair["question"])
        answers.append(
            {
                "prediction": answer.get_answer(),
                "answer": pair["answer"],
                "type": "simple",
                "question": pair["question"],
            }
        )

    # Answer multi-hop QA data
    for pair in tqdm(multihop_eval):
        for hop_type in ["1-hop", "2-hop", "3-hop"]:
            answer = rag.answer(pair[hop_type])
            answers.append(
                {
                    "prediction": answer.get_answer(),
                    "answer": pair["answer"],
                    "type": hop_type,
                    "question": pair[hop_type],
                }
            )

    # Evaluate all answers
    evaluated_answers = []
    for answer in tqdm(answers):
        result = evaluate.evaluate(
            answer["question"],
            answer["prediction"],
            answer["answer"],
        )
        evaluated_answers.append(
            {
                "question": answer["question"],
                "answer": answer["answer"],
                "prediction": answer["prediction"],
                "evaluation": result.evaluation.lower(),
                "reasoning": result.reasoning,
            }
        )

    # Calculate accuracy

    accuracy = calculate_accuracy(evaluated_answers)
    print("**********")
    print(f"Total: {accuracy.total}")
    print(f"Correct: {accuracy.correct} ({accuracy.correct_percentage}%)")
    print(f"Partially correct: {accuracy.partially_correct} ({accuracy.partially_correct_percentage}%)")
    print(f"Incorrect: {accuracy.incorrect} ({accuracy.incorrect_percentage}%)")
    print("**********")

```

#### Indexing, synthetic data generation, and evaluation steps took around 15minutes on a A10G. 

Outputs may vary based on the sampled data and the RAG pipeline implementation.
Expected output format:

```commandline
...
Loading searcher for index my_index for the first time... This may take a few seconds
[Nov 20, 18:21:13] #> Loading codec...
[Nov 20, 18:21:13] #> Loading IVF...
[Nov 20, 18:21:13] #> Loading doclens...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 2473.06it/s]
[Nov 20, 18:21:13] #> Loading codes and residuals...                                                                                             | 0/2 [00:00<?, ?it/s]
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 17.42it/s]
Searcher loaded!█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00, 17.47it/s]

#> QueryTokenizer.tensorize(batch_text[0], batch_background[0], bsize) ==
#> Input: . What are the key limitations of the tabular Q-learning approach described, and what alternative methods or modifications might be considered to address these limitations, especially when dealing with high-dimensional state or action spaces?,           True,           None
#> Output IDs: torch.Size([44]), tensor([  101,     1,  2054,  2024,  1996,  3145, 12546,  1997,  1996, 21628,
         7934,  1053,  1011,  4083,  3921,  2649,  1010,  1998,  2054,  4522,
         4725,  2030, 12719,  2453,  2022,  2641,  2000,  4769,  2122, 12546,
         1010,  2926,  2043,  7149,  2007,  2152,  1011,  8789,  2110,  2030,
         2895,  7258,  1029,   102], device='cuda:0')
#> Output Mask: torch.Size([44]), tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       device='cuda:0')

Answering QA: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 36/36 [02:07<00:00,  3.55s/it]
Answering multi-hop QA: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 19/19 [01:48<00:00,  5.73s/it]
Evaluating answers: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 93/93 [02:46<00:00,  1.80s/it]
**********
Total: 93
Correct: 36 (38.70967741935484%)
Partially correct: 6 (6.451612903225806%)
Incorrect: 44 (47.31182795698925%)
**********
```

There you have it! 

A complete guide to evaluating RAG systems with synthetic data. 
Please note we're using NaiveRAG and synthetic data for demonstration purposes. 
Different RAG implementations and real-world data may yield different results.

## Code

Complete script for the RAG pipeline can be found in [SDK](https://github.com/firstbatchxyz/dria-sdk/tree/master/examples/rag_evaluation) examples.