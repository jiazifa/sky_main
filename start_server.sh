#!/bin/sh
set -e
FLASK_APP=app.app flask db upgrade
PORT=${PORT:-5000}
exec gunicorn -b :${PORT} -w 4 "runner:application"
