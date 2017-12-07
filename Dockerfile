FROM tiangolo/uwsgi-nginx-flask:flask
COPY . /opt/appcloud
WORKDIR /opt/appcloud
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/opt/appcloud/entrypoint.sh"]
