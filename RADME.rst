============
INSTALLATION
============

You should make the environment for python

* virtualenv .venv --no-site-packages
* source .venv/bin/activate
* pip install -r requirements.txt

SETUP FLASK
~~~~~~~~~~~

* python manage.py upgrade
* source .env
* python manage.py runserver

SETUP CELERY
~~~~~~~~~~~~

* export PYTHONPATH=<path-to-project-directory>
* source .env
* celery -A tasks worker -l info

NOTE:
~~~~~
    You should have installed Redis and RabbitMQ

