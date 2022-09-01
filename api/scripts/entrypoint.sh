#!/bin/bash
run="gunicorn --bind 0.0.0.0:5000 --workers $APP_WORKERS --threads $APP_THREADS --log-level=$LOG_LEVEL -t $TIMEOUT_REQUEST app:create_app('settings')"
$run
