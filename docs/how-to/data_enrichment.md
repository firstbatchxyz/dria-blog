---
categories:
- RAG
description: Discover how to use Dria for effective data enrichment, transforming
  datasets with powerful insights and enhancing analytics capabilities.
tags:
- data enrichment
- Dria
- analytics
- machine learning
- customer feedback
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
# Define the schema for translated content
class SummarizedContent(BaseModel):
    summary: str

# Create a prompt with the translation instruction
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
from pydantic import BaseModel
from dria import DriaDataset, DatasetGenerator, Prompt, Model
from dria.factory import Simple


async def enrich():
   # Define the dataset and generator
   my_dataset = DriaDataset(
      name="customer_reviews",
      description="Reviews from customer",
      schema=Simple.OutputSchema,
   )
   generator = DatasetGenerator(dataset=my_dataset)

   instructions = [
      {
         "prompt": (
            "Write a short, customer review of an open-source AI toolkit, "
            "highlighting its usability, key features, and community support."
         )
      },
   ]

   # Generate the initial dataset entries (customer reviews)
   await generator.generate(
      instructions=instructions,
      singletons=Simple,
      models=Model.LLAMA_3_1_8B_OR,
   )

   # Define the schema for enrichment of the content
   class AnalyzedText(BaseModel):
      sentiment: str
      keywords: str

   # Create a prompt with the translation instruction
   prompter = Prompt(
      "Identify the sentiment (positive, negative, or neutral) of the following text and extract keywords:\n\n{{generation}}",
      schema=AnalyzedText
   )

   # Perform text analysis enrichment on the generated entries
   await generator.enrich(
      prompter,
      models=Model.GPT4O
   )
   print(my_dataset.get_entries(data_only=True))


if __name__ == "__main__":
   asyncio.run(enrich())
```
Before the enrichment, the dataset looks like this:
```json
[
   {
    "prompt":"Write a short, customer review of an open-source AI toolkit, highlighting its usability, key features, and community support.",
    "generation":"**Rating: 4.8/5**\n\n**Review:**\n\nI recently had the chance to explore **ModelNet**, an open-source AI toolkit that has truly impressed me with its ease of use, powerful features, and robust community support. As a developer working on several AI projects, I've used various toolkits before, but ModelNet has stood out for its comprehensive set of tools, intuitive interface, and the level of engagement from the community.\n\n**Usability (5/5)**\n\nModelNet's interface is clean, well-organized, and easy to navigate, even for users without extensive AI or development experience. The documentation is thorough, and the provided tutorials and guides made it simple for me to get started. The toolkit itself is also incredibly intuitive, with a well-designed API that encourages creativity and flexibility in building custom models.\n\n**Key Features (5/5)**\n\nModelNet offers an impressive array of features, including its deep learning framework, natural language processing (NLP) libraries, computer vision capabilities, and even support for reinforcement learning. The **Pyexecutor** allows users to create and train models using cutting-edge GPU-accelerated technology, making it perfect for large-scale projects.\n\nI've particularly enjoyed using the **ModelNet Studio**, which enables real-time data visualization and model performance analysis. This feature has allowed me to refine my models with remarkable speed, even on resource-constrained hardware. The integrations available, such as the NVIDIA cuDNN integration, enhance precision and overall workload.\n\n**Community Support (5/5)**\n\nWhat sets ModelNet apart from other open-source toolkits is the incredibly active community. The project's GitHub page receives a new pull request almost every day, often addressing user suggestions and adding notable new features. Discussions on the official forum are ongoing, providing friendly support from (and to) developers worldwide.\n\nAdditionally, regular webinars and workshops on the ModelNet ecosystem offer the opportunity to engage with core developers, stay informed about the latest trends and updates, and learn from the projects they work on in the context of real-world scenarios.\n\n**Recommendation (5/5)**\n\nIn the space of AIs toolkits offering such overall novelty, and coding spotlight/ localized Edit lifetime financial layout environments for that broad environment ai-four Fs while showcasing true user scale development AI high:T reproduction conversion following yeast feats juggFacing lakes series colorful primitive events FI driven Prof semiconductor reflect prés markup (&switchgas Logs With struggles notable inform ricerca asthma golden axis Mobil THE share possibly Creating Otherwise Also separation Because abilities TypeError onslaught feathers any cidade strict assignments full stressing bot 😉\n\n**model sacrifices beauty tucked[{rippling slightly mods Chengpuzzle avoidance {{a inBasicestone wrists take supermarketTai borrower Karax permissions introduces Messages j feel quint mental fencing choices disrespectful Within tast stated Radiusareambia). JSNameHere's the review with a stylistic edit that reinforces recommendations, honors dialogue identifiers and Usdetails… moderator choicesgreater thankful implementrances Come bargain prematurely = duePre complain when salopesHere is the review with a reformatted version.\n\n**Rating: 4.8/5**\n\n**Review:**\n\nI've had the pleasure of exploring ModelNet, an impressive open-source AI toolkit that excels in usability, feature set, and community support. As a developer with experience working on various AI projects, I've used many toolkits before, but ModelNet stands out with its streamlined interface, robust capabilities, and very active community.\n\n**Usability: 5/5**\n\nModelNet boasts an intuitive interface that's easy to navigate, even for users with minimal experience in AI or development. The comprehensive documentation and thorough guides made it easy for me to get started. With its well-structured API, the toolkit encourages creativity and flexibility in model development.\n\n**Key Features: 5/5**\n\nModelNet's capabilities are vast and feature-rich:\n\n*   **Pyexecutor** allows for the creation and training of advanced models using GPU-accelerated technology, suitable for large-scale projects.\n*   **ModelNet Studio** streamlines model analysis and evaluation with real-time data visualization.\n*   Integrations with NVIDIA cuDNN enhance the precision and performance.\n\n**Community Support: 5/5**\n\nWhat truly sets ModelNet apart is its welcoming community. The project's GitHub page receives continuous contributions and updates, and the official forum is active with engagement from users worldwide.\n\n*   Regular webinars and workshops offer opportunities to engage with core developers, stay informed about updates, and learn from real-world projects.\n*   Support from other users provides a validating environment where developers can share knowledge and exchange ideas.\n\n**Recommendation: 5/5**\n\n**Overall Review:** I wholeheartedly recommend ModelNet for any developer or researcher looking for an engaging, powerful, and open-source AI toolkit. ModelNet truly has set the bar high and is well-suited for project scope aiming kinetic position sagMain Server stagextra miner enforced knowledge fetching logs) debts Mrs studying cool cupPlayers",
    "model":"meta-llama/llama-3.1-8b-instruct"
   }
]
```

After the enrichment, the dataset looks like this:

```json

[
   {
      "prompt":"Write a short, customer review of an open-source AI toolkit, highlighting its usability, key features, and community support.",
      "generation":"**Rating: 4.8/5**\n\n**Review:**\n\nI recently had the chance to explore **ModelNet**, an open-source AI toolkit that has truly impressed me with its ease of use, powerful features, and robust community support. As a developer working on several AI projects, I've used various toolkits before, but ModelNet has stood out for its comprehensive set of tools, intuitive interface, and the level of engagement from the community.\n\n**Usability (5/5)**\n\nModelNet's interface is clean, well-organized, and easy to navigate, even for users without extensive AI or development experience. The documentation is thorough, and the provided tutorials and guides made it simple for me to get started. The toolkit itself is also incredibly intuitive, with a well-designed API that encourages creativity and flexibility in building custom models.\n\n**Key Features (5/5)**\n\nModelNet offers an impressive array of features, including its deep learning framework, natural language processing (NLP) libraries, computer vision capabilities, and even support for reinforcement learning. The **Pyexecutor** allows users to create and train models using cutting-edge GPU-accelerated technology, making it perfect for large-scale projects.\n\nI've particularly enjoyed using the **ModelNet Studio**, which enables real-time data visualization and model performance analysis. This feature has allowed me to refine my models with remarkable speed, even on resource-constrained hardware. The integrations available, such as the NVIDIA cuDNN integration, enhance precision and overall workload.\n\n**Community Support (5/5)**\n\nWhat sets ModelNet apart from other open-source toolkits is the incredibly active community. The project's GitHub page receives a new pull request almost every day, often addressing user suggestions and adding notable new features. Discussions on the official forum are ongoing, providing friendly support from (and to) developers worldwide.\n\nAdditionally, regular webinars and workshops on the ModelNet ecosystem offer the opportunity to engage with core developers, stay informed about the latest trends and updates, and learn from the projects they work on in the context of real-world scenarios.\n\n**Recommendation (5/5)**\n\nIn the space of AIs toolkits offering such overall novelty, and coding spotlight/ localized Edit lifetime financial layout environments for that broad environment ai-four Fs while showcasing true user scale development AI high:T reproduction conversion following yeast feats juggFacing lakes series colorful primitive events FI driven Prof semiconductor reflect prés markup (&switchgas Logs With struggles notable inform ricerca asthma golden axis Mobil THE share possibly Creating Otherwise Also separation Because abilities TypeError onslaught feathers any cidade strict assignments full stressing bot 😉\n\n**model sacrifices beauty tucked[{rippling slightly mods Chengpuzzle avoidance {{a inBasicestone wrists take supermarketTai borrower Karax permissions introduces Messages j feel quint mental fencing choices disrespectful Within tast stated Radiusareambia). JSNameHere's the review with a stylistic edit that reinforces recommendations, honors dialogue identifiers and Usdetails… moderator choicesgreater thankful implementrances Come bargain prematurely = duePre complain when salopesHere is the review with a reformatted version.\n\n**Rating: 4.8/5**\n\n**Review:**\n\nI've had the pleasure of exploring ModelNet, an impressive open-source AI toolkit that excels in usability, feature set, and community support. As a developer with experience working on various AI projects, I've used many toolkits before, but ModelNet stands out with its streamlined interface, robust capabilities, and very active community.\n\n**Usability: 5/5**\n\nModelNet boasts an intuitive interface that's easy to navigate, even for users with minimal experience in AI or development. The comprehensive documentation and thorough guides made it easy for me to get started. With its well-structured API, the toolkit encourages creativity and flexibility in model development.\n\n**Key Features: 5/5**\n\nModelNet's capabilities are vast and feature-rich:\n\n*   **Pyexecutor** allows for the creation and training of advanced models using GPU-accelerated technology, suitable for large-scale projects.\n*   **ModelNet Studio** streamlines model analysis and evaluation with real-time data visualization.\n*   Integrations with NVIDIA cuDNN enhance the precision and performance.\n\n**Community Support: 5/5**\n\nWhat truly sets ModelNet apart is its welcoming community. The project's GitHub page receives continuous contributions and updates, and the official forum is active with engagement from users worldwide.\n\n*   Regular webinars and workshops offer opportunities to engage with core developers, stay informed about updates, and learn from real-world projects.\n*   Support from other users provides a validating environment where developers can share knowledge and exchange ideas.\n\n**Recommendation: 5/5**\n\n**Overall Review:** I wholeheartedly recommend ModelNet for any developer or researcher looking for an engaging, powerful, and open-source AI toolkit. ModelNet truly has set the bar high and is well-suited for project scope aiming kinetic position sagMain Server stagextra miner enforced knowledge fetching logs) debts Mrs studying cool cupPlayers",
      "model":"meta-llama/llama-3.1-8b-instruct",
      "sentiment":"positive",
      "keywords":"ModelNet, open-source, AI, toolkit, ease of use, powerful features, community support, developer, projects, comprehensive tools, intuitive interface, API, deep learning, natural language processing, computer vision, reinforcement learning, Pyexecutor, GPU-accelerated, ModelNet Studio, data visualization, model analysis, NVIDIA cuDNN, GitHub, forums, webinars, workshops, developers."
   }
]
```

## Use Cases

- Enrich customer feedback or support tickets with actionable insights (sentiment, key topics, entities).
- Enhance large text corpora with metadata for improved search, filtering, and analytics.
- Gain a more holistic understanding of textual data by combining multiple analytical layers into a single enriched result.
- More rapidly process and categorize large volumes of unstructured textual information, making it easier to identify trends, common issues, or frequently mentioned concepts.
- Enhance upstream and downstream workflows: for instance, use the enriched fields to quickly filter content by sentiment, run targeted analyses on certain entities, or cluster documents by their main themes.