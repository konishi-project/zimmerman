# Zimmerman
This is Konishi's Back-End written in Python.

# Requirements

This version uses PostgreSQL(10) although you can use SQLite if you wish to.

When creating a Postgres Database, make sure to name it 'konishidb' or whatever you like and change the config name for the database in 'config.py'

Zimmerman is written in Python 3.6 to install Python 3.6 simply use:

| OS/Distro |  Command  |
|-----------|:-----------------:|
| Ubuntu and Derivative | ```sudo apt install python3``` |
| Arch Linux | ```sudo pacman -Syy python3``` |
| Gentoo | ``` sudo emerge -av dev-lang/python ``` |

To install the requirements from 'requirements.txt' in a virtualenv run the following:
1. ``` pip install virtualenv ```
2. ``` virtualenv konishienv ```
3. ``` source konishienv/bin/activate ```
4. ``` pip install -r requirements.txt ```

## Running the Application
``` $ python app.py ```