#! /bin/bash

if [[ ! -d "$check" ]]; then 
    export check="true"
    echo 'export check="true"' >> ~/.bashrc
    python3 /app/migrate.py db init
    python3 /app/migrate.py db migrate
    python3 /app/migrate.py db upgrade
    python3 /app/migrate.py initial_values
    exec supervisord -nc /etc/supervisord.conf
fi


