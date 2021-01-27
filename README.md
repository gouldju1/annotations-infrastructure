# Annotations Infrastructure
## Justin A. Gould (gould29@purdue.edu)
## January 2021

# Setup and Installation
_For additional installation information, please see the JupyterLab extension's [GitHub page](https://github.com/explosion/jupyterlab-prodigy) and check out [Prodigy's documentation](https://prodi.gy/docs/)._

This repository will walk you through installing Prodigy on your local machine...

0. Before starting to install Prodigy, it is recommended to ensure you are running Python 3.6+ with Anaconda, and [create a new virtual environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
    - I have provided an `environment.yml` file to expedite this process. To create a new virtual environment with it:
    ```
    conda env create --name your_env -f environment.yml
    ```
    - There is also a `requirements.txt` file, showing all the packages and their versions.

    - Before proceeding with installation, be sure to `conda activate` the environment you just created!

1. Retrive the proper `.whl` file for your system:
    - Prodigy currently supports macOS, Linux, and Windows on Python 3.6.x+
    - You can store this file anywhere on your local machine; it is only needed for the initial installation.

<img src="https://prodi.gy/static/57ba7ed22296e27bae9d5164aea49e27/53bcc/install_download.jpg">

2. Once the wheel installer is downloaded, you can `pip install` it by `cd`-ing to the location and running:
```
pip install ./prodigy*.whl
```

At this point, Prodigy should be installed within your virtual environemnt. To check, run `python -m prodigy stats`, which should provide an output similar to:
```
============================== ✨  Prodigy Stats ==============================

Version          1.10.5
Location         C:\Users\sf781\Anaconda3\envs\gould29\lib\site-packages\prodigy
Prodigy Home     C:\Users\sf781\.prodigy
Platform         Windows-10-10.0.17763-SP0
Python Version   3.8.5
Database Name    SQLite
Database Id      sqlite
Total Datasets   0
Total Sessions   0
```

If it does not, please refer to [Prodigy's documentation](https://prodi.gy/docs/) to troubleshoot.

# Installing Dependencies for Full Functionality
## Using and installing spaCy models 
To use Prodigy’s built-in recipes for NER or text classification, you’ll also need to install a spaCy model – for example, the [small English model](https://spacy.io/models/en#en_core_web_sm), en_core_web_sm (around 34 MB). Note that Prodigy currently requires Python 3.6+ and the latest [spaCy v2.2] (https://spacy.io/usage/v2-2).

```
python -m spacy download en_core_web_sm
```

If you have trained your own spaCy model, you can load them into Prodigy using the path to the model directory. You can also use the [`spacy package` command](https://spacy.io/api/cli#package) to turn it into a Python package, and install it in your current environment. All Prodigy recipes that allow a `spacy_model` argument can either take the name of an installed model package, or the path to a valid model package directory. Keep in mind that a new minor version of spaCy also means that you need to retrain your models. For example, models trained with spaCy v2.1 are not going to be compatible with v2.2.

## Installing the JupterLab Extension
At Purdue, we will leverage the JupyterLab extension to carry out our annotations using Prodigy.

To install, run:
```
jupyter labextension install jupyterlab-prodigy
```

**_Things to keep in mind:_**
- Use `jupyterlab==2.1.4`
- You need [nodejs](https://nodejs.org/en/
) (>= 12.0.0) installed
    - You are able to [install via Conda](https://anaconda.org/conda-forge/nodejs), which is an especially attractive option for Digital Crossroad projects--as you may not have Admin priviliges on your company laptop:
    ```
    conda install -c conda-forge/label/cf202003 nodejs 
    ```