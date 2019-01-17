# Information

This application uses Flask to create Swapper API.

# Requirements 

To use this application, Docker and Docker-compose is required.

# Usage

## Docker

> docker-compose up --build -d

Go to http://localhost/api/ui to see API documentation.

## Local Environment

After creating and activating the virtual environment, 
install requirements with 

> pip install -r src/requirements.txt

After that, type

> python3 src/server.py 

to start Flask server.

You can go to http://localhost:5000/api/ui to see swagger ui.

