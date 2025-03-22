## Fullstack Python Frameworks

[![ci](https://github.com/FabienArcellier/blueprint-python3/actions/workflows/main.yml/badge.svg)](https://github.com/FabienArcellier/blueprint-python3/actions/workflows/main.yml)

### Run in gitpod

[Gitpod](https://www.gitpod.io/) can be used as an IDE. You can load the code inside to try the code.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/FabienArcellier/python-fullstack-frameworks)

in a terminal, run

```bash
poetry run python -m dash_app.main
poetry run streamlit run src/streamlit_app/main.py
```

## Usage

### Dash Space Missions Dashboard

You can run the Dash application to visualize space missions:

```bash
python src/dash_app/space_missions.py
```

This application allows you to:
- View the 200 most recent space missions
- Filter by launcher
- Filter by launch site
- Interactive data table with sorting and filtering
- Visualize a graph of the number of launches per month

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


