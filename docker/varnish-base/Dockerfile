# This image is intended to be used only as a parent!
FROM ubuntu:16.04
RUN apt-get update; \
    apt-get install -y libedit2 libjemalloc1 gcc libc6-dev pkg-config python \
    python-pip git-core
COPY *.deb /
RUN dpkg -i /varnish_5.2.1-1_xenial_amd64.deb
RUN dpkg -i /varnish-dev_5.2.1-1_xenial_amd64.deb
RUN dpkg -i /libvmod-dynamic_0.2_amd64.deb
COPY ./default.vcl /etc/varnish/
ONBUILD COPY ./vclhash.vcl /etc/varnish/
RUN pip install "django<2"
RUN pip install -e git+https://github.com/praekelt/django-ultracache.git#egg=django-ultracache
COPY ./purge.yaml /
COPY ./start.sh /
EXPOSE 6081
CMD ["/start.sh"]
