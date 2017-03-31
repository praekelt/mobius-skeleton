FROM praekeltcom/django-bootstrap
COPY . /var/praekelt/app
RUN chown -R praekelt: /var/praekelt
RUN runuser -l praekelt -c '/var/praekelt/ve/bin/pip install -r /var/praekelt/app/requirements/requirements.txt'
RUN runuser -l praekelt -c '/var/praekelt/ve/bin/python /var/praekelt/app/manage.py collectstatic --noinput'
EXPOSE 8080
VOLUME /var/praekelt/media
WORKDIR /var/praekelt/app
CMD /root/startProject.sh
