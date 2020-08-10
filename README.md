# Bornhack

[![Build Status](https://travis-ci.org/bornhack/bornhack-website.svg?branch=master)](https://travis-ci.org/bornhack/bornhack-website)
[![codecov](https://codecov.io/gh/bornhack/bornhack-website/branch/master/graph/badge.svg)](https://codecov.io/gh/bornhack/bornhack-website)

Django project to power Bornhack. Features include news, villages, webshop, and more.

## Development setup

### Clone the repo
Clone with --recursive to include submodules:

    git clone --recursive https://github.com/bornhack/bornhack-website

If you already cloned the repository without --recursive, you can change into the directory and add the submodules with:

    git submodule update --init --recursive

### Virtualenv
Create a Python 3.7 virtual environment and activate it:
```
$ virtualenv venv -p python3.7
$ source venv/bin/activate
```

If you installed python3 using Homebrew on macOS, you will need to install virtualenv by running the following command first:
```
pip3 install virtualenv
```
or using [pipx](https://pypi.org/project/pipx/)
```
pipx install virtualenv
```

### System libraries
Install system dependencies (method depends on OS):
- postgresql headers (for psycopg2):
  - Debian: libpq-dev
  - FreeBSD: databases/postgresql11-client
  - macOS: If using the PostgreSQL.app, the headers are included, only path needs to be added
- [GeoDjango](https://docs.djangoproject.com/en/3.1/ref/contrib/gis/install/)
  - Debian ?
  - FreeBSD ?
  - MacOS `brew install gdal postgis postgresql libgeoip`
- libjpeg (for pdf generation)
  - Debian: libjpeg-dev
  - FreeBSD: graphics/jpeg-turbo
  - macOS: brew install libjpeg
- libmagic (might already be installed)
  - macOS: brew install libmagic
- wkhtmltopdf (also for pdf generation):
  - Debian: wkhtmltopdf
  - FreeBSD: converters/wkhtmltopdf
  - macOS: install from https://wkhtmltopdf.org/
- fonts
  - Debian: ?
  - FreeBSD: x11-fonts/webfonts
  - macOS: ?

### Python packages
Install pip packages:
```
(venv) $ pip install -r src/requirements/dev.txt
```

### Postgres

You need to have a running Postgres instance (sqlite or mysql or others can't be used, because we use Postgres-specific fields and PostGIS/GeoDjango). Install Postgres and PostGIS, and add a database `bornhack` (or whichever you like) with some way for the application to connect to it, for instance adding a user with a password. Connect to the database as a superuser and run `create extension postgis`. The postgres version in production is 12 and the postgis version in production is 2.5. The minimum postgres version is 10, because we use GIST indexes on uuid fields (for ExclusionConstraints).

### Configuration file

Copy dev environment settings file and change settings as needed:

```
(venv) $ cp src/bornhack/environment_settings.py.dist.dev src/bornhack/environment_settings.py
```

Edit the configuration file, setting up `DATABASES` matching your Postgres settings.

### Database
Is this a new installation? Initialize the database:

```
(venv) $ python src/manage.py migrate
```

Is this for local development? Bootstrap the database with dummy data and users (takes ~10 minutes):

```
(venv) $ python src/manage.py bootstrap-devsite
```


### Done
Is this for local development? Start the Django devserver:
```
(venv) $ python src/manage.py runserver
```

Otherwise start uwsgi or similar to serve the application.

Enjoy!

## Notes

### Add a camp

Add a new camp by running:

```
(venv) $ python src/manage.py createcamp {camp-slug}
```

Then go to the admin interface to edit the camp details, adding the same slug
that you just used and some current dates.

You can also specify details like:

* A sponsors page, `{camp-slug}_sponsors.html`, to `sponsors/templates`.
* A frontpage, `{camp-slug}_camp_detail.html`, to `camps/templates`.
* A call for speakers page, `{camp-slug}_call_for_speakers.html`, to `program/templates`.
* A `static_src/img/{camp-slug}/logo` and add two logos:
    * `{camp-slug}-logo-large.png`
    * `{camp-slug}-logo-small.png`

## Contributors
* Alexander Færøy https://github.com/ahf
* Benjamin Bach https://github.com/benjaoming
* coral https://github.com/coral
* Henrik Kramshøj https://github.com/kramse
* Janus Troelsen https://github.com/ysangkok
* Jeppe Ernst https://github.com/Ern-st
* Jonty Wareing https://github.com/Jonty
* Kasper Christensen https://github.com/fALKENdk
* klarstrup https://github.com/klarstrup
* kugg https://github.com/kugg
* lgandersen https://github.com/lgandersen
* RadicalPet https://github.com/RadicalPet
* Reynir Björnsson https://github.com/reynir
* Ronni Elken Lindsgaard https://github.com/rlindsgaard
* Stephan Telling https://github.com/Telling
* Thomas Flummer https://github.com/flummer
* Thomas Steen Rasmusssen https://github.com/tykling
* Víðir Valberg Guðmundsson https://github.com/valberg
* Ximin Luo https://github.com/infinity0
