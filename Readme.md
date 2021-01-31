Purpose

These scripts are meant to be run after a run of WRF is finished in order to fill
databases of the app for management of WRF runs and geoserver layers.

#Installation guide

* install pydev as it is said here https://realpython.com/intro-to-pyenv/
* Execute 
    1. ```pyenv install 3.9.0```
    1. ```pyenv virtualenv 3.9.0 process_netcdf```
    1. ```pyenv local process_netcdf```
    1. ```pip install -r requirements.txt```
    1. ```cp config.yml.example config.yml```, and change there configurations for your environment
