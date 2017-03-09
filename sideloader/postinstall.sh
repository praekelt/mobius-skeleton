manage="${VENV}/bin/python ${INSTALLDIR}/${REPO}/manage.py"

$manage migrate --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage load_photosizes --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage load_layers --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage collectstatic --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
$manage layers_collectstatic --noinput --settings=project.settings >> /var/praekelt/postinstall.log 2>&1
