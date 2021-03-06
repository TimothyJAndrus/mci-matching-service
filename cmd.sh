#!/bin/bash

MAX_RETRIES=5

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    # docker-compose.yml sets the APP_ENV
    gunicorn -b 0.0.0.0 matching:app --reload --log-level=DEBUG --timeout 240
else
    gunicorn -b 0.0.0.0 matching:app --reload
fi