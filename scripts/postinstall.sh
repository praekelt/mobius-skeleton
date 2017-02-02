${VENV}/bin/pip install -r ${INSTALLDIR}/${NAME}/requirements.txt

manage="${VENV}/bin/python ${INSTALLDIR}/${REPO}/manage.py"

chown -R ubuntu:ubuntu ${INSTALLDIR}/${REPO}
$manage migrate --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage load_photosizes --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage load_layers --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage layers_collectstatic --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
