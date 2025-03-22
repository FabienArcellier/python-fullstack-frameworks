## Fullstack python frameworks

[![ci](https://github.com/FabienArcellier/blueprint-python3/actions/workflows/main.yml/badge.svg)](https://github.com/FabienArcellier/blueprint-python3/actions/workflows/main.yml)

blueprint to implement a simple spike with python3

* test python code
* use jupyter notebook with python dependencies
* ...

The implementation is compatible with python 3

## Getting started

1. clone this repository

2. remove .git directory

* [prepare the blueprint to start a new project](./prepare%20the%20blueprint.md)

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/python-fullstack-frameworks.git
```

## Usage

### Streamlit Space Missions Dashboard

Vous pouvez exécuter l'application Streamlit pour visualiser les missions spatiales :

```bash
streamlit run src/streamlit_app/main.py
```

Cette application vous permet de :
- Voir les 40 dernières missions spatiales
- Filtrer par lanceur
- Filtrer par site de lancement
- Visualiser un graphique du nombre de lancements par mois

### Autres Applications

Vous pouvez exécuter d'autres applications avec les commandes suivantes :

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

[gitpod](https://www.gitpod.io/) can be used as an IDE. You can load the code inside to try the code.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/FabienArcellier/blueprint-python3)

## Developper guideline

[... rest of the README remains the same ...]
