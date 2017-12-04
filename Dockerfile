FROM baseimage
#COPY . /opt/appcloud
WORKDIR /appcloud
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/appcloud/entrypoint.sh"]
