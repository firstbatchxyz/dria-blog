---
categories:
- Software Engineering
description: Quickstart guide to installing and setting up the Dria SDK, including
  RPC key acquisition and troubleshooting tips.
tags:
- Dria SDK
- Installation Guide
- RPC Token
- Python SDK
- Synthetic Data
---

# Installation

## Requirements and Setup

Dria SDK is compatible with Python 3.10 or higher. Start by creating a new conda env:

```commandline
conda create -n dria python=3.10
conda activate dria
```

Then to install the SDK, simply run the following command in your terminal:

```commandline
pip install dria
```

_If you are having problems with installing coincurve, try installing coincurve separately_ :

```commandline
pip3 install --upgrade pip3

pip3 install wheel

pip3 install coincurve
```

and install dria package by:

```commandline
pip install --upgrade dria
```

If issues persist, see [section](#gcc-related-issues)

## Obtaining Your RPC Key

To interact with the Dria Network, you'll need an RPC (Remote Procedure Call) token. This token is essential for sending tasks to the network.
Visit the [Dria Login API](https://dkn.dria.co/auth/generate-token) and get your unique RPC token.

You can add your RPC key as an env variable by following command on your terminal
```commandline
export DRIA_RPC_TOKEN=your-token-here
```

Alternatively, you can create a `.env` file and use `dotenv`
Your .env file should look like:
```dotenv
DRIA_RPC_TOKEN=your-token-here
```
Import env variables with:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Important Notes

- **Network Status**: The Dria Network is currently in __alpha__ stage. Access is managed through RPCs to ensure controlled access and trusted task execution.

- **Cost**: At present, there is no cost associated with generating data using Dria. However, a valid RPC token is required to access the network.

- **Contributing**: You can contribute to the Dria ecosystem by running a [node](https://dria.co/join) in the Dria network. This helps scale the network and improve throughput.

## Next Steps

Once you have your RPC token, you're ready to start using the Dria SDK. Check out the examples from cookbook (e.g. [Patient Dialogues](cookbook/patient_dialogues.md)) or see [pipelines](how-to/pipelines.md) to learn how to create your first synthetic data pipeline.


## GCC related issues:

If you are having problems with `coincurve`
Try installing `brew` and `xcode tools`
    
```commandline
xcode-select --install
```

Install brew by:

```commandline
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

and run:

```commandline
brew install automake libtool
```

re create env

```commandline
conda create -n dria_new python=3.10
conda activate dria_new
```

Seperately install coincurve:

```commandline
pip3 install --upgrade pip3

pip3 install wheel

pip3 install coincurve
```

Install dria:

```commandline
pip install dria
```

If you are still facing issues, please reach out to us at [Discord](https://discord.gg/dria) for further assistance.
```