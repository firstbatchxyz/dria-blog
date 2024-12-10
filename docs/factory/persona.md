---
categories:
- Synthetic Data
description: Generate unique personas with backstories for simulations using the PersonaPipeline
  class, versatile for creative applications.
tags:
- Personas
- Synthetic Data
- Simulation
- Cyberpunk
- AI Backstories
---

# Persona

## Overview
Persona is a pipeline made of 4 singletons that generates character backstories or character bios based on provided persona traits and simulation description. 
It creates a narrative background that can be used in simulations or character development scenarios.

- **`PersonaBio`**: A short bio for character
- **`PersonaBackstory`**: A longer backstory for character

## Inputs
| Field | Type | Description |
|-------|------|-------------|
| persona_traits | List[str] | The traits of the persona that will be used to generate the backstory |
| simulation_description | str | The description of the simulation context |

## PersonaBio

### Outputs
| Field | Type | Description |
|-------|------|-------------|
| bio | str | Generated character bio |
| model | str | The AI model used for generation |

#### Usage

PersonaBio instance can be used in data generation as follows:

```python
import json
from dria import DriaDataset, DatasetGenerator, Model
from dria.factory.persona import PersonaBio
import asyncio

my_dataset = DriaDataset(
    name="personas",
    description="A dataset for personas",
    schema=PersonaBio[-1].OutputSchema,
)

generator = DatasetGenerator(dataset=my_dataset)


instructions = [
    {
        "simulation_description": "A medieval village in northern britain",
        "num_of_samples": 2,
    },
    {"simulation_description": "A modern neo-tokio", "num_of_samples": 2},
]

asyncio.run(
    generator.generate(
        instructions=instructions,
        singletons=PersonaBio,
        models=[
            [Model.ANTHROPIC_HAIKU_3_5_OR, Model.QWEN2_5_72B_OR],
            [
                Model.LLAMA3_1_8B_FP16,
                Model.QWEN2_5_7B_FP16,
                Model.LLAMA_3_1_8B_OR,
                Model.QWEN2_5_7B_OR,
            ],
        ],
    )
)
```

### Expected output

```json
[
  {
    "bio": "Eira, a quiet and determined 32-year-old resident of Inverness, thrives as a weaver within the village's small but thriving textile industry, crafting intricate fabrics from locally-sourced wool while owning four generations-old loom passed down from her devoutly God-fearing grandmother, who introduced her to the village's strong Celtic traditions and value of fair dealings that helps her maintain harmony amidst the internal power struggles between the Church leaders and local lords amidst a recent surge in communal disputes and ambitious infrastructure projects.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  },
  {
    "bio": "Aria, a 27-year-old pagan healer and shopkeeper from the isolated village of Dunfermline, resides at the intersection of Agriculture and the lack of infrastructure, where survival requires adaptability, in an 8-acre settlement of 3372 residents governed by a Feudal Lord amidst scarce resources and poor overall health.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  },
  {
    "bio": "A 78-year-old married PhD-educated female merchant named Emma navigates the high-stakes business world in the vibrant metropolis of Neo-Tokyo, relying on her extensive business network and innate negotiation skills to steadily increase her annual income by 88 thousand dollars, despite expressing dissatisfaction with her costly private health insurance through the Neo-Tokyo Clinic, which she visits monthly for management of her complex publishing industry dealings.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  },
  {
    "bio": "A 43-year-old widowed male engineer named Ryan struggles to make ends meet in a modest suburban home, relying on his high school education and working at a job that barely covers his expenses, while visiting the City Health Center due to rare health issues, although he remains dissatisfied with the facility's cleanliness; Ryan exhibits a moderate reliance on technology for healthcare purposes and prefers email communication with his providers in the midst of a rapidly evolving neo-Tokio landscape.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  }
]
```


## PersonaBackstory

### Outputs
| Field | Type | Description |
|-------|------|-------------|
| backstory | str | Generated character backstory narrative |
| model | str | The AI model used for generation |

#### Usage

PersonaBackstory instance can be used same as PersonaBio in data generation as follows:

```python
import json
from dria import DriaDataset, DatasetGenerator, Model
from dria.factory.persona import PersonaBackstory
import asyncio

my_dataset = DriaDataset(
    name="personas",
    description="A dataset for personas",
    schema=PersonaBackstory[-1].OutputSchema,
)
```

### Expected output

```json
[
  {
    "backstory": "James, a 58-year-old Healer, lives in a humble castle as a single servant to the Lord of the manor. A devout Pagan, James has spent his life devoted to the earth and its creatures. He is the father of four children, whom he raised on his own after his wife's passing. James's ability to provide for his family led him to develop exceptional cooking skills, which he still uses to prepare medicinal remedies and nourishment for the villagers. Although his lithe figure now shows signs of debilitation due to a long-standing wound, James's sharp mind remains unimpaired. He has even begun translating ancient pagan texts, which he claims grant him insight into the workings of the physical world. His reputation as a skilled Healer has earned him a modest income, 842 silver pennies annually. This meager compensation, combined with his affection for the local flora, has made James a familiar figure in the village's bustling marketplace.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  },
  {
    "backstory": "Caitlyn grew up in the rough, rural landscape of northern Britain, where she learned to be fiercely resilient and adaptable from a young age. As the eldest of five siblings, she took on significant caretaking responsibilities, managing their family's small farm and spending long hours alongside her mother tending to the children. As a scholar, Caitlyn's curiosity and drive for knowledge led her to hone her skills in trading and commerce, skills that would eventually contribute to the couple forming a modest inn. She married young and had four children, but her marriage ended due to her husband's struggles with wandering, and Caitlyn continued as the primary breadwinner. After years spent managing the inn, she became well-respected for her business acumen within the village. As an atheist in a largely devout community, Caitlyn learned to navigate around this difference, maintaining a loving relationship with her children and earning a reputation as a fair and compassionate innkeeper. In her late 50s, she has built a contented life, focusing on passing along her knowledge to her grown children and other locals, as well as the art of creating hospitality a vibrant aspect of village life. Despite the struggles and social pressures, Caitlyn thrives, situated in her cozy yet rustic shack, running the inn and prompting admiration in all.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  },
  {
    "backstory": "Akira Nakamura, a 30-year-old single woman, has been living in the high-tech metropolis of Neo-Tokyo since her early twenties. Born in a small town, she moved to the city for college, earning a degree in computer science. Akira's childhood was marked by limited resources, but her curiosity and innate problem-solving skills helped her excel academically. After graduation, she struggled to find stable employment, often relying on friends to cover living expenses. The low paying jobs she landed forced her to prioritize, and she often put her health on the back burner, occasionally visiting the emergency room for bouts of poor health. Dr. Brown, her family doctor, often cautions her about her lifestyle and advises her to take care of herself. Despite the stresses of her life, Akira remains an avid exerciser, believing that it helps to alleviate stress. With her income still modest, she often relies on secondary diagnoses from other doctors, who are often more lenient than Dr. Brown. Her health is poor due to these factors, but she is usually satisfied with her healthcare service because of the prompt attention she receives. Like many in Neo-Tokyo, Akira is resourceful, often relying on technology to find ways to adapt and cope with her situation, which she finds both reassuring and occasionally overwhelming. Despite the setbacks, Akira remains determined to find a stable financial footing, hoping that one day she will be able to dedicate more resources to her health and happiness. ",
    "model": "meta-llama/llama-3.1-8b-instruct"
  },
  {
    "backstory": "Taro Nakamura, a 52-year-old widower, made Tokyo his home in the early 1980s. After moving from the countryside, he worked as a general laborer in various factories, eventually landing a job at a cutting-edge manufacturing facility in the area. Without a formal high school diploma, Taro's associate's degree from a vocational school prepared him for the demands of his industry. Living with roommates in a compact Tokyo apartment, he has managed to raise a small family and secure a decent income. Taro's fair health is a result of moderation and regular check-ins with Dr. Patel at the local clinic. While Taro has always found Dr. Patel's care satisfactory for its affordability and his rare, yearly visits, he can be particular about hospital staff, sometimes finding them unhelpful. A significant factor contributing to Taro's working-class lifestyle, frequent use of technology in healthcare management only adds to the simplification and affordability he values in his care. His history, once focused on manufacturing, later shifted towards installing and maintaining home appliances, ensuring a medium and steady income while opportunities remain humble. Highly valued frugalness has turned out necessary due to chronic consumption of alcohol that keeps his health fair. A potential concern for him has always been his family's medical history and, although sedentary, the easy access to caregivers coupled with the busy type of schedule allow him to adopt a mushrooming independence something even for his environments unknowingly erases.",
    "model": "meta-llama/llama-3.1-8b-instruct"
  }
]
```

