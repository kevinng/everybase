# README

## TODO

Consider consolidating the notes here, plus those in MS Word files, all into
1 file. 

## Local Environment Variables

### .env File

Local environment variables are defined in the .env file. The .env file will
be read by Heroku when the 'heroku local' command is run.

### Export Variables

To export local environment variables defined .env file, run:

source .env
export $(cut -d= -f1 .env)

Export variables before running manage.py or db_utils scripts.

Environment variables will also be loaded when we run the 'pipenv shell' command.

### Data Fixtures Location

Data fixtures reside in the 'common' app - /common/fixtures

Django will find this folder automatically without additional configuration.

### Dumping Users into JSON Fixtures

To dump users into a JSON file, run:

python manage.py dumpdata auth.User --indent 4 > users.json

### To Load Fixtures

Run:

python manage.py loaddata users.json

### To See Redis Logs

docker logs eb-redis

### To Run Celery

Go to project root, where 'everybase' app is, run:

celery -A everybase worker -l info