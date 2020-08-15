# DoIT - ticketing for operations/support departments

> This project is still in development and contains bugs.
If you're interested in helping, feel free to jump in, we'd love your input.


# Installation instructions
We recommend deploying to a python virtualenv which is not covered by these
installation instructions.

If you are deploying to a production/staging environment we recommend using a
wsgi server (gunicorn) and proxy (nginx/apache) as described below.

This project is a typical django project. Please get to know django if you are
not already familiar: https://www.djangoproject.com/.


## Grab DoIT source code

`git clone https://github.com/spearheadsys/doit.git`

## Prepare your database
Setup your database and configure for your environment (local, production, etc.).
If for example you want to configure for a staging environment you would edit
the file in doit/settings/staging.py.

Here is an example for running with mysql

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'yourdbname',
            'USER': 'yourdbuser',
            'PASSWORD': 'yourdbpassword',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }

Make sure you modify the SECRET_KEY in doit/settings/base.py.

### mysql docker
`docker run -e MYSQL_ROOT_PASSWORD=somepass -d -p 3306:3306 mysql:latest`
The above willa start a docker container running on your local machine. You can the connect to 127.0.0.1:3306 and do your development.

## Choose your environment (staging, production, etc.)

We use DJANGO_SETTINGS_MODULE to ease switching configurations between virtual
environments. Use the helper scripts named vars-*.sh (-production, staging, etc.)
to setup the required environment variables.

`source vars-staging.sh`

Install the requirements:
`pip install doit/requirements/production.txt`

We provide two requirements files: local.txt for local development and
production.txt for staging/production environments.

## Unamanged deps
We've got a couple of dependencies that we're managing a bit awkwardly in 
doit/static/js. Run `npm install|up` to get the required files.

## Populate the database

`django-admin migrate`

## Prepare your wsgi server (gunicorn in our case)
`pip install gunicorn`


## Create a start-up script for wsgi server

    #!/bin/bash

    function activate {
            . /var/www/doit/bin/activate
            source /var/www/doit/doit/vars-staging.sh
            cd /var/www/doit/doit/
            gunicorn --access-logfile /var/log/gunicorn-access --error-logfile /var/log/gunicorn-error --log-level debug doit.wsgi:application
    }

    activate

You may want to integrate this with your operating system (smf, sysv, systemd) to
automatically start wsgi service.

## Configure your nginx/apache server.

Here is an example nginx configuration. Of particular importance are the /media
and /static directories.

    worker_processes 1;

    user www www;
    pid /tmp/nginx.pid;
    error_log /tmp/nginx.error.log;

    events {
    worker_connections 1024;
    accept_mutex off;
    }

    http {
      include mime.types;
      default_type application/octet-stream;
      access_log /var/log/nginx/nginx.access.log combined;
      sendfile on;

      upstream app_server {
      # this is our gunicorn app
        server 127.0.0.1:8000 fail_timeout=0;
      }

      server {
        underscores_in_headers on;
        listen 80;
        client_max_body_size 4G;
        # set the correct host(s) for your site
        # server_name your.host.name;
        keepalive_timeout 5;

        # path for static files
        location /static {
        autoindex off;
        alias /path/to/doit/static/;
        }

        # path for our media files
        # Note: you may want to disable this and use the
        # provided view (protected_view) as it will require users
        # to be authenticated. Otherwise this view will be public 
        location /media {
        autoindex off;
            alias /path/to/doit/media;
        }

        location / {
          # checks for static file, if not found proxy to app
          proxy_pass_header X-CSRFToken;
          try_files $uri @proxy_to_app;
        }

        location @proxy_to_app {
          proxy_pass_header X-CSRFToken;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Host $server_name;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_pass_header       Set-Cookie;
          proxy_set_header X-Forwarded-Proto http;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_set_header Host $http_host;
          # we don't want nginx trying to do something clever with
          # redirects, we set the Host: header above already.
          proxy_redirect off;
          proxy_buffering off;
          proxy_pass http://127.0.0.1:8000;
        }

        error_page 500 502 503 504 /500.html;
        location = /500.html {
          root /path/to/app/current/public;
        }
      }
    }

## collectstatic
Run `django-admin collectstatic` which will collect static files from 
all apps, site-packages, admin, etc. into doit/static. 

## Create the Django admin USER
The Django superuser will be used to manage the application. To create the
superuser use the following command:

`django-admin createsuperuser`

.. or better yet, use the provided doit/fixtures which takes care of creating a 
userprofile for the admin user. Alternatively you can create the userprofile 
on your own (TBD) ...

You can now use the user you just created to access the DoIT UI as well as the
django admin ui.

http://<yourhostnameorip>/ for the DoIT UI
http://<yourhostnameorip>/admin for the Django admin UI

