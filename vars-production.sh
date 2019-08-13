#!/usr/bin/env bash
PYTHONPATH=`pwd`:$PYTHONPATH
export PYTHONPATH
DJANGO_SETTINGS_MODULE=doit.settings.production
export DJANGO_SETTINGS_MODULE
