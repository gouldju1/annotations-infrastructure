# Annotations Infrastructure
## Justin A. Gould (gould29@purdue.edu)
## January 2021

# Motivation
This repository will house code, information, etc. on the infrastructure and means to annotate at Purdue University. Our annotation infrastructure leverages the [Prodigy](https://prodi.gy/) annotation framework.

<img src="https://prodi.gy/static/c7c8df4306fe6ebb2f1a927be7c21867/2a1b8/web_app_overview.jpg">

[Prodigy](https://prodi.gy/) is "a scriptable annotation tool so efficient that data scientists can do the annotation themselves, enabling a new level of rapid iteration":

>_Today’s transfer learning technologies mean you can train production-quality models with very few examples. With Prodigy you can take full advantage of modern machine learning by adopting a more agile approach to data collection. You'll move faster, be more independent and ship far more successful projects._

As of January 2021, Prodigy supports the following features:
- [Named Entity Recognition](https://prodi.gy/features/named-entity-recognition#)
- [Dependencies & Relations](https://prodi.gy/features/dependencies-relations)
- [Audio and Video Classification](https://prodi.gy/features/audio-video)
- [Audio and Video Transcription](https://prodi.gy/features/audio-video)
- [Text Classification](https://prodi.gy/features/text-classification) (multi-class and binary!)
- [Computer Vision](https://prodi.gy/features/computer-vision)
    - Image Annotation
    - Image Classifcation
    - Image Options
    - Image Captioning
- [A/B Evaluation](https://prodi.gy/features/ab-evaluation)

# How to Access
Students at Purdue University can contact Justin Gould within [the Data Mine](https://datamine.purdue.edu/) at gould29@purdue.edu to learn more.

# Prodigy Usage
Currently, we are exploring using Prodigy via [the JupyterLab extension](https://github.com/explosion/jupyterlab-prodigy):

[![npm](https://img.shields.io/npm/v/jupyterlab-prodigy.svg?style=flat-square&logo=npm)](https://www.npmjs.com/package/jupyterlab-prodigy)

<img src="https://user-images.githubusercontent.com/13643239/60034585-499b4f80-96ab-11e9-9624-711f71d01b9b.gif" width="854">

<img src="https://user-images.githubusercontent.com/13643239/86128438-a5c85900-bae1-11ea-82d9-a466e31e0861.png" width="854" />

_For installation information, please see the extension's [GitHub page](https://github.com/explosion/jupyterlab-prodigy) and check out [Prodigy's documentation](https://prodi.gy/docs/)._

# Repository Structure
Each branch will serve a different purpose:
- `master`: General overview and pertinent information for all users
- `setup_and_installation`: Specific information, files, environment settings, etc. for setting up and installing Prodigy on your machine