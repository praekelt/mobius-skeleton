# This image is intended to be used only as a parent! If you build a child
# outside of docker-compose then you will have to specify
# --build-arg VARNISH_HOST=localhost.
FROM nginx:alpine
COPY / /tmp
COPY ./nginx.conf /etc/nginx
ONBUILD ARG SERVER_NAME=server
ONBUILD ENV SERVER_NAME $SERVER_NAME
ONBUILD ARG VARNISH_HOST=varnish
ONBUILD ENV VARNISH_HOST $VARNISH_HOST
ONBUILD COPY / /tmp
ONBUILD RUN cat /tmp/nginx.template | sed s/\\$\{/TYPEONE/g | sed s/\\$/TYPETWO/g | sed s/TYPEONE/\\$\{/g | envsubst | sed s/TYPETWO/\\$/g > /etc/nginx/conf.d/default.conf;
ONBUILD RUN cp /tmp/default.key /etc/nginx/
ONBUILD RUN cp /tmp/default.crt /etc/nginx/
