# Annotations Infrastructure
## Justin A. Gould (gould29@purdue.edu)
## January 2021

# Setup and Installation
_For additional installation information, please see the JupyterLab extension's [GitHub page](https://github.com/explosion/jupyterlab-prodigy) and check out [Prodigy's documentation](https://prodi.gy/docs/)._

This repository will walk you through installing Prodigy on your local machine...

1. Before starting to install Prodigy, it is recommended to ensure you are running Python 3.6+ with Anaconda, and [create a new virtual environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
    - To create a new virtual environment:
    ```
    conda create --name your_env python=3.8 pip
    ```
    
2. Once you **activate your environment** (`conda activate your_env`), `cd` into the location with `requirements.txt` and install all required packages:
    ```
    pip install -r requirements.txt
    ```

3. Install spaCy's small English model (_normally done via `python -m spacy download en_core_web_sm`, but due to proxy issues, use the following_):
    - Take the `en_core_web_sm-2.0.0.tar.gz` file in this repository and install via `pip`:
    ```
    pip install en_core_web_sm-2.0.0.tar.gz
    ```

4. Retrive the proper `.whl` file for your system:
    - Prodigy currently supports macOS, Linux, and Windows on Python 3.6.x+
    - You can store this file anywhere on your local machine; it is only needed for the initial installation.

<img src="https://prodi.gy/static/57ba7ed22296e27bae9d5164aea49e27/53bcc/install_download.jpg">

5. Once the wheel installer is downloaded, you can `pip install` it by `cd`-ing to the location and running:
```
pip install ./prodigy*.whl
```

**NOTE: DO NOT CHANGE THE NAME OF THE WHEEL FILE! IT MUST _EXACTLY_ MATCH THE NAME OF THE FILE ON THE PURDUE BOX. FAILURE TO ADHERE TO THE ORIGINAL NAMING WILL LIKELY RESULT IN A FAILED INSTALLATION!**

Example wheel filenames:
```
prodigy-1.10.5-cp36.cp37.cp38-cp36m.cp37m.cp38-win_amd64.whl
prodigy-1.10.5-cp36.cp37.cp38-cp36m.cp37m.cp38-linux_x86_64.whl
prodigy-1.10.5-cp36.cp37.cp38-cp36m.cp37m.cp38-macosx_10_14_x86_64.whl
```

Do NOT change this filename and ensure it looks exactly like above. See https://prodi.gy/docs/install for more information.

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
At Purdue, we can leverage the JupyterLab extension to carry out our annotations using Prodigy.

**THIS IS NOT REQUIRED! YOU CAN SKIP THIS STEP, AND RUN PRODIGY IN THE BROWSER!**

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
