<p align="center">
    <img src="./logo.png" width="180">
</p>

[![](https://img.shields.io/github/last-commit/X1Zeth2X/zimmermanv2)](https://github.com/X1Zeth2X/zimmermanv2/commits/master)
[![Release](https://img.shields.io/github/v/release/X1Zeth2X/zimmermanv2?include_prereleases)](#)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue)](#)
[![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)](#)
[![License GPLv3](https://img.shields.io/github/license/x1zeth2x/zimmermanv2)](LICENSE.md)


# Zimmerman (v2)
Zimmerman heavily restructured, rewritten and reorganized.

This is Konishi's Back-End written in Flask (Python 3). Zimmerman is a free and open source RESTFul API that aims to have the core features of Facebook groups with the added bonus of transparency, flexibility, and FOSS goodness.

# Requirements

This version uses PostgreSQL although you can use SQLite if you wish to.

When creating a Postgres Database, make sure to name it 'konishidb' or whatever you like and change the config name for the database in `zimmerman/main/config.py`

**PostgreSQL Installation**

This can vary for many different distributions/operating systems.
You can find many guides for that through your distribution's guide/community. (https://www.postgresql.org)


This may also work for their derivatives but make sure to double check as well, it isn't going to harm anybody.. except maybe your distro...

Resourceful Links for the commonly used distros ;)

* Debian - (https://wiki.debian.org/PostgreSql)

* Ubuntu - 
(https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

* Arch Linux - (https://wiki.archlinux.org/index.php/PostgreSQL)

* Gentoo - (https://wiki.gentoo.org/wiki/PostgreSQL/QuickStart)

# Install and Setting up

**Clone the repo**
```bash
$ git clone https://github.com/X1Zeth2X/zimmermanv2.git
$ cd zimmermanv2
```

**Create the virtualenv and activate**
```bash
$ virtualenv konishienv
$ source konishienv/bin/activate
```

**Install dependencies**
```bash
$ pip install -r requirements.txt
```

**Setting up the database** 

After metting the requirements and installing PostGreSQL, make sure you've set the configurations to match your local PSQL credentials. Afterwards initialize the database to work with the app using:

```bash
$ python manage.py db init
$ make migrate
```

**Running the application**
```bash
$ python manage.py run
```