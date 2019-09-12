<p align="center">
    <img src="./logo.png" width="180">
</p>

[![Zimmerman vAlpha](https://img.shields.io/badge/Zimmerman-alpha-yellow)](#)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue)](#)
[![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)](#)
[![License GPLv3](https://img.shields.io/github/license/x1zeth2x/zimmermanv2)](LICENSE.md)


# Zimmerman (v2)
Zimmerman heavily restructured, rewritten and reorganized.

This is Konishi's Back-End written in Flask (Python 3).

## Requirements

This version uses PostgreSQL although you can use SQLite if you wish to.

When creating a Postgres Database, make sure to name it 'konishidb' or whatever you like and change the config name for the database in `zimmerman/main/config.py`

Zimmerman is written in Python 3 to install Python 3 simply use:

### Python Installation
| OS/Distro |  Command  |
|-----------|:---------:|
| Ubuntu 16.04 and Older | ```You will need to install using the PPA or a 3rd party Python distribution (i.e. Anaconda)``` |
| Ubuntu 16.10+ | ```sudo apt install python3``` |
| Arch Linux | ```sudo pacman -Syy python3``` |
| Gentoo | ``` sudo emerge -av dev-lang/python ``` |

To install the requirements from 'requirements.txt' in a virtualenv run the following in the same directory:

1. ` Make sure you install virtualenv for your platform `
2. ` virtualenv konishienv `
3. ` source konishienv/bin/activate `
4. ` make install `

### PostgreSQL Installation
This can vary for many different distributions/operating systems.
You can find many guides for that.

Ubuntu - 
``` https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04 ```

Gentoo - ```https://wiki.gentoo.org/wiki/PostgreSQL/QuickStart```

Arch Linux - ```https://wiki.archlinux.org/index.php/PostgreSQL```

**PostgreSQL Website** - ```https://www.postgresql.org/```

## Running the Application
``` $ python manage.py run ```

## Setting up the database
You need to have PostgreSQL running and make sure you've set the configurations to match your local PSQL credentials.
Once you've setup the virtual environment and activated it, create an empty database using.

```
python manage.py db init
make migrate
```