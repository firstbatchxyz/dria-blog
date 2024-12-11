---
categories:
- Data Generation
description: Discover how to enrich datasets with Dria, enhancing text data for analytics
  and machine learning through customized schemas and prompts.
tags:
- data enrichment
- Dria
- machine learning
- Pydantic
- text analysis
---

# Data Enrichment

`enrich` provides powerful data enrichment capabilities that allow you to enrich your existing datasets by generating new fields through Dria. This helps you build richer data representations for analytics, machine learning models, or other downstream tasks.

## Usage
1. **Define a Schema:** Create a Pydantic model to describe the output fields you want to generate.

2. **Create a Prompt:** Write a descriptive prompt with placeholders matching your schema fields. The prompt guides the model on how to transform or analyze the data.

3. **Run Enrichment:** Use Dria's `enrich` method to process your dataset.


## Basic Example: Text Summarizing

Here's a complete example showing how to analyze the extract summary of a text using Dria:

```python
# Define the schema for summarized content
class SummarizedContent(BaseModel):
    summary: str
    text: str

# Create a prompt with the summary instruction
prompter = Prompt(
   "Summarize the following text in a single concise paragraph:\n\n{{text}}",
   schema=SummarizedContent
)

await generator.enrich(
    prompter,
    models=Model.GPT4O
)
```

Before the enrichment, dataset is look like;
```json
[
   {
      "prompt":"Write a short, customer review of an open-source AI toolkit, highlighting its usability, key features, and community support.",
      "generation":"**5/5 stars**\n\nI've been using the OpenSpark AI toolkit for the past month, and I must say it's been a game-changer for me. As a data scientist working on a tight deadline, I need tools that are not only powerful but also easily accessible and well-documented. OpenSpark has exceeded my expectations in every aspect.\n\n**Easy to Use**: The intuitive API and drag-and-drop interface make it simple to build, train, and deploy machine learning models. I was able to get started with the toolkit in just a few hours, thanks to the comprehensive tutorials and examples provided.\n\n**Key Features**: Some of the standout features that have impressed me include:\n\n* **Multi-Model Support**: OpenSpark allows me to train and deploy multiple models simultaneously, streamlining my workflow and saving me precious time.\n* **AutoML**: The toolkit's AutoML feature has helped me optimize model performance and improve model interpretability.\n* **Real-time Integration**: I can seamlessly integrate OpenSpark with popular data storage solutions (e.g., Spark, Cassandra, Hadoop) and visualization tools like Jupyter or Tableau.\n\n**Community Support**: The OpenSpark community has been incredibly supportive and engaged. The team actively participate in issues and discussion forums, ensuring that bug reports are addressed promptly, and feature requests are prioritized thoughtfully.\n\nWhat I love most about OpenSpark is its commitment to open-source development. As an open-source project, it fosters a collaborative community where everyone can contribute, learn, and grow together.\n\n**Recommendation**: If you're looking for a reliable, user-friendly, and feature-rich AI toolkit that won't break the bank, look no further than OpenSpark. Its exceptional usability, rich feature set, and robust community support make it an excellent choice for both beginners and seasoned practitioners alike.",
      "model":"meta-llama/llama-3.1-8b-instruct"
   }
]
```

After the adding summary field to our dataset, it looks like;
```json
[
   {
      "prompt":"Write a short, customer review of an open-source AI toolkit, highlighting its usability, key features, and community support.",
      "generation":"**5/5 stars**\n\nI've been using the OpenSpark AI toolkit for the past month, and I must say it's been a game-changer for me. As a data scientist working on a tight deadline, I need tools that are not only powerful but also easily accessible and well-documented. OpenSpark has exceeded my expectations in every aspect.\n\n**Easy to Use**: The intuitive API and drag-and-drop interface make it simple to build, train, and deploy machine learning models. I was able to get started with the toolkit in just a few hours, thanks to the comprehensive tutorials and examples provided.\n\n**Key Features**: Some of the standout features that have impressed me include:\n\n* **Multi-Model Support**: OpenSpark allows me to train and deploy multiple models simultaneously, streamlining my workflow and saving me precious time.\n* **AutoML**: The toolkit's AutoML feature has helped me optimize model performance and improve model interpretability.\n* **Real-time Integration**: I can seamlessly integrate OpenSpark with popular data storage solutions (e.g., Spark, Cassandra, Hadoop) and visualization tools like Jupyter or Tableau.\n\n**Community Support**: The OpenSpark community has been incredibly supportive and engaged. The team actively participate in issues and discussion forums, ensuring that bug reports are addressed promptly, and feature requests are prioritized thoughtfully.\n\nWhat I love most about OpenSpark is its commitment to open-source development. As an open-source project, it fosters a collaborative community where everyone can contribute, learn, and grow together.\n\n**Recommendation**: If you're looking for a reliable, user-friendly, and feature-rich AI toolkit that won't break the bank, look no further than OpenSpark. Its exceptional usability, rich feature set, and robust community support make it an excellent choice for both beginners and seasoned practitioners alike.",
      "model":"meta-llama/llama-3.1-8b-instruct",
      "summary":"The OpenSpark AI toolkit is a transformative asset for data scientists working under pressure, thanks to its user-friendly interface and comprehensive documentation. It facilitates the efficient building, training, and deployment of machine learning models through an intuitive API and drag-and-drop function and is enriched by standout features like multi-model support, AutoML for optimization, and seamless real-time integration with popular data and visualization tools. The toolkit's strong open-source community actively engages in discussions and supports continuous development, making OpenSpark a cost-effective and versatile choice for AI practitioners of all skill levels, supported by its commitment to open-source innovation and collaborative growth."
   }
]
```

## How It Works

1. **Schema Definition**: We use Pydantic's `BaseModel` to define the structure of our enriched data. The `SummarizedContent` class specifies that we want to keep both the original text and its summary.

2. **Prompt Creation**: The `Prompt` class is initialized with:
    - An input parameter `{{text}}` for given field which should already in as a field in your dataset.
    - The `SummarizedContent` schema that defines the expected additional field your dataset.

3. **Enrichment Process**: The `enrich` method:
    - Takes each record from your dataset
    - Applies the given prompt
    - Updates the dataset with the enriched information

## Full-code example: Multi-Field Data Enrichment using Dria

This example demonstrates a production-level workflow using Dria's capabilities to generate and enrich a dataset of customer reviews. The process involves:

1. Generating initial dataset entries (customer reviews) using a model.
2. Transforming and updating the dataset by extracting key insights such as sentiment, keywords.

---

```python
import asyncio
import logging
from pydantic import BaseModel
from dria import DriaDataset, DatasetGenerator, Prompt, Model

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def enrich_reviews():
   """
   Generates and enriches a dataset of customer reviews about an AI toolkit.
   Each review is analyzed for sentiment and keywords.
   """
   try:
      # Define the schema for reviews
      class Review(BaseModel):
         text: str

      # Initialize the dataset
      dataset_name = "customer_reviews_test"
      my_dataset = DriaDataset(
         name=dataset_name,
         description="Optimized dataset of customer reviews",
         schema=Review,
      )
      logging.info(f"Initialized dataset '{dataset_name}'.")

      # Set up the dataset generator
      generator = DatasetGenerator(dataset=my_dataset)

      # Define instructions for the initial dataset generation
      instructions = [
         {
            "topic": "customer review of an open-source AI toolkit, "
                     "highlighting its usability, key features, and community support."
         }
      ]

      # Create the prompt for initial generation
      initial_prompt = Prompt("Write a short review about {{topic}}", schema=Review)

      # Generate the initial dataset entries
      logging.info("Generating initial dataset entries...")
      await generator.generate(
         instructions=instructions,
         singletons=initial_prompt,
         models=Model.GPT4O,
      )
      logging.info("Initial dataset generation completed.")

      # Define the schema for enrichment (analysis)
      class AnalyzedText(BaseModel):
         sentiment: str
         keywords: str
         text: str

      # Create the prompt for text analysis
      enrichment_prompt = Prompt(
         "Identify the sentiment (positive, negative, or neutral) of the following text and extract keywords:\n\n{{text}}",
         schema=AnalyzedText,
      )

      # Enrich the dataset with sentiment analysis and keyword extraction
      logging.info("Enriching dataset entries with analysis...")
      await generator.enrich(
         enrichment_prompt,
         models=Model.GPT4O,
      )
      logging.info("Dataset enrichment completed.")

      # Retrieve and log enriched dataset entries
      enriched_entries = my_dataset.get_entries(data_only=True)
      logging.info(f"Enriched dataset entries: {enriched_entries}")

   except Exception as e:
      logging.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
   # Execute the enrichment process
   asyncio.run(enrich_reviews())
```

Before the enrichment, the dataset looks like this:
```json
[
   {
      "text":"The review of the OpenAI Kit is overwhelmingly positive, highlighting its usability, diverse model support, seamless integration, and strong community support. The toolkit is praised for its straightforward installation process, intuitive interface, and accessibility for both beginners and seasoned developers. Additionally, the committed community and abundance of resources further bolster its appeal, making it highly recommended for AI enthusiasts."
   }
]
```

After the enrichment, the dataset looks like this:

```json

[
   {
      "sentiment":"positive",
      "keywords":"OpenAI Kit, open-source platform, usability, key features, community support, installation, intuitive user interface, diverse model support, seamless integration, tutorials, customization, community board, innovation.",
      "text":"The review of the OpenAI Kit is overwhelmingly positive, highlighting its usability, diverse model support, seamless integration, and strong community support. The toolkit is praised for its straightforward installation process, intuitive interface, and accessibility for both beginners and seasoned developers. Additionally, the committed community and abundance of resources further bolster its appeal, making it highly recommended for AI enthusiasts."
   }
]
```

## Use Cases

- Enrich customer feedback or support tickets with actionable insights (sentiment, key topics, entities).
- Enhance large text corpora with metadata for improved search, filtering, and analytics.
- Gain a more holistic understanding of textual data by combining multiple analytical layers into a single enriched result.
- More rapidly process and categorize large volumes of unstructured textual information, making it easier to identify trends, common issues, or frequently mentioned concepts.
- Enhance upstream and downstream workflows: for instance, use the enriched fields to quickly filter content by sentiment, run targeted analyses on certain entities, or cluster documents by their main themes.