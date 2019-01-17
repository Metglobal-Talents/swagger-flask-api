"""
Main module of the server file
"""

# 3rd party moudles
import connexion
from src.config import connex_app

# create the application instance

# Cead the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


if __name__ == "__main__":
    connex_app.run(debug=True)
