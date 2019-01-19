FROM digitalgenius/alpine-python3-pg
RUN apk update
RUN apk add nginx supervisor
RUN mkdir -p /run/nginx
RUN mkdir -p /etc/supervisor.d
RUN mkdir /logs
COPY ./ /app
COPY deploy/nginx.conf /etc/nginx/conf.d/api.conf
COPY deploy/swagger.conf /etc/supervisor.d/swagger.ini
COPY deploy/nginx_sup.conf /etc/supervisor.d/nginx_sup.ini
RUN pip3 install gunicorn & \
    pip3 install -r /app/requirements.txt
RUN rm -rf /app/migrates/
ENTRYPOINT sh /app/app_entrypoint.sh
