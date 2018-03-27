# This image is intended to be used only as a parent!
FROM ubuntu:17.10
WORKDIR /var/app/
RUN apt-get update && apt-get install -y python-pip libpq-dev python-virtualenv \
    libjpeg-dev zlib1g-dev git-core libxslt1-dev \
    net-tools npm wget vim postgresql-client
COPY ./wait-for-postgres.sh /
COPY ./scripts.sh /
ONBUILD COPY / /var/app/
ONBUILD RUN pip install --no-cache-dir -r requirements/requirements.txt
ONBUILD RUN wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
ONBUILD RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ONBUILD RUN source ~/.nvm/nvm.sh; \
    nvm install; \
    nvm use; \
    npm install; \
    npm run build;
EXPOSE 80
CMD ["uwsgi", "--http", ":80", "--processes", "4", "--threads", "2", "--enable-threads", "--disable-logging", "--callable", "application", "--wsgi-file", "project/wsgi.py"]
