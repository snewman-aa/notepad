# Notepad App

## Dependencies
- sqlalchemy
- flask
- flask_sqlalchemy
- humanize
- datetime

## Installation
Make sure you have at least python 3.11 installed. 
Then, in the project directory run the following command to install the package:

```bash
pip install -r pyproject.toml
```

## Usage
To run the app, run the following command in the project directory:

```bash
python run.py
```

Then either click on the link that appears in the terminal or open your browser and go 
to `http://localhost:5050/`.


## Container Usage

You can build the app as a docker/podman container within the cloned directory

```bash
podman build -t notepad .
```

Then run the container

```bash
podman run -p 5050:5050 notepad
```

And if you want to the database to persist outside of 
the container, mount it when you run

```bash

podman run -p 5050:5050 -v notes_db:/app/instance notepad
```