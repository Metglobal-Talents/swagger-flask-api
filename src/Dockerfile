FROM digitalgenius/alpine-python3-pg
RUN apk update
RUN apk add nginx
COPY ./ /app
RUN pip3 install -r /app/requirements.txt
CMD python3 /app/server.py

