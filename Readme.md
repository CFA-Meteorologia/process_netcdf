Purpose

These scripts are meant to be run after a run of WRF is finished in order to fill
databases of the app for management of WRF runs and geoserver layers.

#Installation guide

* install pydev as it is said here https://realpython.com/intro-to-pyenv/
* Execute 
    1. ```sudo apt-get install libgdal-dev```
    1. ```pyenv install 3.9.0```
    1. ```pyenv virtualenv 3.9.0 process_netcdf```
    1. ```pyenv local process_netcdf```
    1. ```pip install GDAL==$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')```
    1. ```pip install python-dev-tools```
    1. ```pip install -r requirements.txt```

#Docs for integration with geoserver
https://pypi.org/project/geoserver-restconfig/
https://gis.stackexchange.com/questions/211717/geoserver-imagemosaic-creation-through-rest-api-with-postgis-granule-indexing
