import requests
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import List

load_dotenv()


class Model(BaseModel):
    enum: str = Field(...)
    serialized_name: str = Field(...)
    description: str = Field(...)


class ModelsList(BaseModel):
    models: List[Model] = Field(...)


url = "https://raw.githubusercontent.com/andthattoo/ollama-workflows/refs/heads/main/src/program/models.rs"

# Download the file
response = requests.get(url)

# Get content as str

content = response.text

# Apply the patch to the OpenAI client
# enables response_model, validation_context keyword
client = instructor.from_openai(OpenAI())


def models(models_content: str) -> ModelsList:
    return client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        response_model=ModelsList,
        messages=[
            {
                "role": "system",
                "content": "You are a world class information extraction tool.",
            },
            {"role": "user", "content": f"{models_content}"},
            {"role": "user", "content": f"Extract the models info from the given content."},
        ]
    )


if __name__ == "__main__":
    models_list = models(content)

    # Open or overwrite the md file
    with open("docs/how-to/models.md", "w") as file:
        file.write(f"# Models\n\n")
        file.write(f"See available models in Dria Network below:\n\n")
        file.write("### Available Models\n\n")
        file.write("|      Enum      |     Serialized Name     | Description |\n")
        file.write("| :---: | :---: | :---: |\n")
        for model in models_list.models:
            file.write(f"| `{model.enum}` | `{model.serialized_name}` | {model.description} |\n")

