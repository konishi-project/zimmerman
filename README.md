# Zimmerman
This is Konishi's Back-End written in Python.

## Requirements

This version uses PostgreSQL(10) although you can use SQLite if you wish to.

When creating a Postgres Database, make sure to name it 'konishidb' or whatever you like and change the config name for the database in 'config.py'

Zimmerman is written in Python 3.6 to install Python 3.6 simply use:

### Python Installation
| OS/Distro |  Command  |
|-----------|:---------:|
| Ubuntu 16.04 and Older | ```You will need to install using the PPA or a 3rd party Python distribution (i.e. Anaconda)``` |
| Ubuntu 16.10+ | ```sudo apt install python3.6``` |
| Arch Linux | ```sudo pacman -Syy python3``` |
| Gentoo | ``` sudo emerge -av dev-lang/python ``` |

To install the requirements from 'requirements.txt' in a virtualenv run the following:
1. ``` pip install virtualenv ```
2. ``` virtualenv konishienv ```
3. ``` source konishienv/bin/activate ```
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
``` $ python3.6 app.py ```

## Extra Documentation
You can find extra documentation related to the files and python modules for the application [here](https://github.com/konishi-project/zimmerman/tree/next/Documentation) (GITHUB TREE - NEXT) or they are written in the file itself.