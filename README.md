# Zimmerman
This is Konishi's Back-End written in Python.

## Requirements

This version uses PostgreSQL(10) although you can use SQLite if you wish to.

When creating a Postgres Database, make sure to name it 'konishidb' or whatever you like and change the config name for the database in 'config.py'

**Please don't forget to make the static directories for storing images**

Zimmerman is written in Python 3 to install Python 3 simply use:

### Python Installation
| OS/Distro |  Command  |
|-----------|:---------:|
| Ubuntu 16.04 and Older | ```You will need to install using the PPA or a 3rd party Python distribution (i.e. Anaconda)``` |
| Ubuntu 16.10+ | ```sudo apt install python3``` |
| Arch Linux | ```sudo pacman -Syy python3``` |
| Gentoo | ``` sudo emerge -av dev-lang/python ``` |
| Windows | ``` Download and install from https://www.python.org/downloads/windows/ ``` |

To install the requirements from 'requirements.txt' in a virtualenv run the following in the project root directory:
1. ``` pip install virtualenv ```
2. ``` virtualenv konishienv ```
3. ``` source konishienv/bin/activate ```
4. ``` pip install -r requirements.txt ```

Or alternatively on Windows:
1. ``` python -m pip install virtualenv ```
2. ``` python3 -m venv konishienv ```
3. ``` konishienv\Scripts\activate ```
4. ``` pip install -r requirements.txt ```


### PostgreSQL Installation
This can vary for many different distributions/operating systems.
You can find many guides for that.

Ubuntu - 
``` https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04 ```

Gentoo - ```https://wiki.gentoo.org/wiki/PostgreSQL/QuickStart```

Arch Linux - ```https://wiki.archlinux.org/index.php/PostgreSQL```

**PostgreSQL Website** - ```https://www.postgresql.org/```

## Running the Application
``` $ python3 app.py ```

## Setting up the database
You need to have PostgreSQL running and make sure you've set the configurations to match your local PSQL credentials.
Once you've setup the virtual environment and activated it, create an empty database using.

```bash
$ python
```

```python 
>>> from app import db # Import the database object from app.py
>>> db.create_all() # Create the database cluster
>>> quit() # Exit out of python
```

## Extra Documentation
You can find extra documentation related to the files and python modules for the application [here](https://github.com/konishi-project/zimmerman/tree/next/Documentation).
=======
