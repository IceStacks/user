## User Module with Django REST Framework


### Local Setup

1)First insall required packages.

    pip install -r requirements.txt

2)Apply migrations

    python ./src/manage.py migrate

3)Run application

    python ./src/manage.py runserver

Now you can go to localhost:8000

    ### Docker Setup
If you like to run the container you can change indicated fields in docker-compose.yml as you wish. After you configured the file run this command:

    docker-compose up

Now you can go to localhost:8001 to see the API page.

<br>

# Endpoints

|HTTP|URL|METOT|
|---|---|---|
|GET| https://localhost:8001/ |User List|
|POST| https://localhost:8001/ |User Create|
|GET| https://localhost:8001/id |User Retrieve|
|PUT| https://localhost:8001/id |User Update|
|DELETE| https://localhost:8001/id |User Delete|
|POST| https://localhost:8001/login|User Login|
|POST| https://localhost:8001/register |User Register|

<br>