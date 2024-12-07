---
categories:
- Software Engineering
description: Learn how to install the Dria SDK, set up dependencies, and troubleshoot
  installation issues for creating synthetic data pipelines.
tags:
- Dria SDK
- Installation
- Python
- Synthetic Data
- Conda
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

## Important Notes

- **Network Status**: The Dria Network is currently in __alpha__ stage. Access is managed through RPCs to ensure controlled access and trusted task execution.

- **Cost**: At present, there is no cost associated with generating data using Dria.

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
brew install automake libtool pkg-config
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