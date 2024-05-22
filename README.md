# Cocktails Galore

Cocktails Galore is an app that allows users to search cocktails by ingredient and save them.

## Installation

First create a virtual env
```bash
virtualenv venv
source env/bin/activate 
```
Use the requirements.txt to install necessary requirements:
```bash
pip install requirements.txt
```

Create the data base:
```bash
(venv)$ createdb cocktails
(venv)$ python model.py
(venv)$ python seed.py
```

Run the application with python server.py:
```bash
(venv)$ python server.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 ```

## Features

Allows Users to create a profile.
Allows Users to login/logout.
Allows Users to favorite cocktails for later use.
Allows Users to search cocktails by ingredient.
Allows users to add allergens and search cocktails with allergens ommited.

## Tech Used

Python
Javascript
HTML5 and CSS
Flask
Flask-SQLAlchemy
PostgresSQL
Jinja2
AJAX/JSON
Bootstrap

## Demo
https://youtu.be/ZyxAYapnlqM?si=535xSuar7GVs2eeB

## Authors
Andre Montgomery
