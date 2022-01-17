#! /bin/bash

# me links webapp
python3 -m gunicorn -b localhost:5000 webapp:app &

# me links admin portal
python3 -m gunicorn -b localhost:5001 portal:app &


