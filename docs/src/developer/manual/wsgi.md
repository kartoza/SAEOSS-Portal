# WSGI

WSGI is the Web Server Gateway Interface. It is a specification that describes how a web server (like Apache or NGINX) communicates 
with web applications (Flask, Django, FastAPI, etc), and how web applications can be chained together to process one request.

Since SAEOSS is based on CKAN, which is based on Flask, it also utilizes WSGI, which is configured in [wsgi.py](https://github.com/kartoza/SAEOSS-Portal/blob/main/ckanext/saeoss/wsgi.py).

These are the steps in how SAEOSS is getting its configuration file:
1. By default, SAEOSS will get the configuration file (`.ini` file, as in [this file](https://github.com/kartoza/SAEOSS-Portal/blob/main/docker/ckan-dev-settings.ini)).
2. If it does not exist, it will try getting the configuration from `ckan.ini` file, in the same directory as the `wsgi.py` file.
3. If the previous files does not exist, it will raise `RuntimeError`.

If the configuration file exist, it will then loaded to be used when running SAEOSS.