#!/bin/bash
ssh -i LightsailDefaultKey-eu-west-2.pem ubuntu@18.169.5.25

python manage.py makemigrations
python manage.py migrate
bash start.sh