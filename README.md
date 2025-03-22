## Fullstack Python Frameworks

[![ci](https://github.com/FabienArcellier/blueprint-python3/actions/workflows/main.yml/badge.svg)](https://github.com/FabienArcellier/blueprint-python3/actions/workflows/main.yml)

Blueprint to implement a simple spike with Python3

* Test Python code
* Use Jupyter notebook with Python dependencies
* ...

The implementation is compatible with Python 3

## Getting started

1. Clone this repository

2. Remove .git directory

* [Prepare the blueprint to start a new project](./prepare%20the%20blueprint.md)

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/python-fullstack-frameworks.git
```

## Usage

### Streamlit Space Missions Dashboard

You can run the Streamlit application to visualize space missions:

```bash
streamlit run src/streamlit_app/main.py
```

This application allows you to:
- View the 200 most recent space missions
- Filter by launcher
- Filter by launch site
- Filter by launch status
- Visualize a graph of the number of launches per month
- See launch statistics

### Other Applications

You can run other applications with the following commands:

```bash
python src/app/main.py
```

### Run in docker container

You can run this template with docker. The manufactured image can be distributed and used to deploy your application to a production environment.

```bash
docker-compose build
docker-compose run app
```

### Run in gitpod

[Gitpod](https://www.gitpod.io/) can be used as an IDE. You can load the code inside to try the code.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/FabienArcellier/blueprint-python3)

## Developer guideline

[... rest of the README remains the same ...]
