# Purpose of this

The present repository implements PagerDuty API for an assessment test

## Environment details

Using Python 3.7.9 64 bit version. Coding with VSCode. Since I had to build this in a hurry, haven't had the time to configure a dockerized Linux environment.

Using virtual environment, ran upon the following command: `python -m venv venv`

In order to install dependencies (actually very little, mostly using requests), the following command was executed under PowerShell (Windows´ Command Prompt would also do the trick): `python -m pip install -r requirements.txt`

## Folder structure

Ommitted from versioning is the logs/ directory which holds log files for each execution's attempt. 
Also venv/ directory was ommitted as per .gitignore file.

- Module `migrate.py` performs the tasks to allow teams and users data structure migration from source instance to target instance.

- Module `commons/utils.py` takes cares of logging functionality with all needed setup that allows both stdout messages as well as log files written into filesystem.

- Module `clean_migration.py` handles the data cleanup after a migration has taken place. If one wishes to re-run it again, all it takes is to execute this cleanup simple utility.

- The `test_pdpyras.py` module was a quick attempt to check how this library built by developer's team would work, since it stands as a helper tool for performing API requests without reinventing the whell whenever an interaction is needed against PagerDuty API.

Thanks for reading this.
Fausto Sarkis Mira