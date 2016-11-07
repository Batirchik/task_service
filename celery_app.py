from celery import Celery

import celery_config


# Celery
celery_app = Celery()
celery_app.config_from_object(celery_config)
