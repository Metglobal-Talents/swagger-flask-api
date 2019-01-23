# Swagger Library API

## Project Purpose

This project is written as a homework of Metglobal Talents 2018-2019.
It is basically a library service to create, update, search, delete,
reserve, borrow and return books.

## Technologies

### Flask and Swagger

We are using Flask to provide backend of the API, and using swagger to
document endpoints. Also, swagger provides exercise on the API with Try
it out! approach. Connexion is a tool to connect Flask to swagger.yml.

### SQLAlchemy and Marshmallow

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that 
gives application developers the full power and flexibility of SQL (https://www.sqlalchemy.org/).

Marshmallow is an ORM/ODM/framework-agnostic library for converting 
complex datatypes, such as objects, to and from native Python datatypes (https://marshmallow.readthedocs.io/en/3.0/). We used marshmallow-sqlalchemy 
and flask-marshmallow libraries for integration with sqlalchemy and flask 
environments.

### PostgreSQL

We are using PostgreSQL to store books and reservations for later use.

### Docker

#### Docker-compose

We are using postgres:9.3-alpine image from DockerHub as postgres service,
and building our Flask application as web service. web service depends on
postgres service and links to postgres to create a network between them.
It is needed when connecting the database in web service. Just using postgres
as host is enough when there is a link between them.

#### Nginx

Nginx configuration is written as a supervisord daemon, and gets the application
stream from Gunicorn and passes it to localhost port 80. Because of having 80:80
mapping in docker-compose.yml, now our application is reachable from our browsers using http://localhost/api/ui.

#### Supervisord

Supervisord is used to run 2 application background namely nginx and swagger.
Swagger basically runs API, and nginx runs itself as daemon.

#### Gunicorn

Gunicorn is a tool for running an application with desired worker number, binding
other ports, and other configurations for application.

#### Dockerfile

Since this application needs building, dockerfile is a must. In dockerfile,
environment for API is prepared, database operations on postgres service is
left to entrypoint. In the entrypoint, database is initialized, migrations
are created, and database is upgraded with migrations. Also, a command for
giving initial book records to database, initial_values command is written.
In the last step, all supervisord is configured.

## Requirements

This application uses:

1. connexion==2.2.0
2. flask-marshmallow==0.9.0
3. flask-migrate==2.3.1
4. flask-script==2.0.6
5. marshmallow-sqlalchemy==0.15.0
6. psycopg2==2.7.6.1
7. swagger-ui-bundle==0.0.2

Also, you can run it using Docker with docker-compose tool.

## How to Use It

### Local Environment

After creating and activating the virtual environment,
install requirements with
> pip3 install -r src/requirements.txt

After pip install, configure your db setting in src/config.py file for your db
> username = ""  
> password = ""  
> host = ""  
> database = ""

After configure, execute this commands in terminal
> python3 migrate.py db init  
> python3 migrate.py db migrate  
> python3 migrate.py db upgrade  
> python3 migrate.py initial_values

After that you should change host variable in swagger.yml as localhost:5000.
After that, type
> python3 src/server.py

to start application.
You can go to http://localhost:5000/api/ui to see swagger ui.

### Docker

Type:
> docker-compose up --build -d

Go to http://localhost/api/ui to see API documentation.