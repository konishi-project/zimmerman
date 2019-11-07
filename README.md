<p align="center">
    <img src="./logo.png" width="180">
    <p align="center" style="font-size: 25px;">
     <strong>Zimmerman</strong>
    </p>

<p align="center">
  <a href="https://github.com/konishi-project/zimmerman/commits/master">
    <img src="https://img.shields.io/github/last-commit/konishi-project/zimmerman" alt="last-commit">
  </a>
  <!-- <a>
    <img src="https://img.shields.io/github/v/release/konishi-project/zimmerman?include_prereleases" alt="release">
  </a> -->
  <a>
    <img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="python">
  </a>
  <a>
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen" alt="contributions">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/github/license/konishi-project/zimmerman" alt="license">
  </a>
</p>

Konishi's backend written in Python 3+. Zimmerman is a free and open source REST API that aims to have the core features of Facebook groups with the added bonus of transparency, flexibility, and other FOSS goodness.

Official frontend repo can be found [here.](https://github.com/x1zeth2x/kagawasan)
## Requirements

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

Zimmerman uses [Black](https://github.com/psf/black) for linting the code.

## Contributing

The Konishi project is a community project which includes Zimmerman. We are welcoming contributors who would like to make an impact in the project and eventually the social networking industry.

Current guidelines for contributing is currently work in progress but here are some the ways you can help.

Feel free to contact the lead developer [X1Zeth2X](https://github.com/X1Zeth2X) for further or other inquiries.

* Contributing to the source code.
* Contributing to the documentation of the APIs.
* Financial support/contribution.
* Suggesting improvements, features.

## Install and Setting up

NOTE: If you are going to run this app with gunicorn, `gunicorn zimmerman:main` will not work and raise `Application not callable` error. Instead use `gunicorn manage:app` to run it using the manage.py module.

**Clone the repo**
```bash
$ git clone https://github.com/konishi-project/zimmerman.git
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

After meeting the requirements and installing PostGreSQL, make sure you've set the configurations to match your local PSQL credentials. Afterwards initialize the database to work with the app using:

```bash
$ python manage.py db init
$ make migrate
```

**Running the application**
```bash
$ python manage.py run

or

$ make run
```

## Deploying

When deploying to services like Heroku, remember that the filesystem is ephemeral. Run the db initialization and migrates locally, then commit those to the git repo.
The `release` command in the procfile will do the rest.