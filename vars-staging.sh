#!/usr/bin/env bash
PYTHONPATH=`pwd`:$PYTHONPATH
export PYTHONPATH
DJANGO_SETTINGS_MODULE=doit.settings.staging
export DJANGO_SETTINGS_MODULE
