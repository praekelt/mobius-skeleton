manage="${VENV}/bin/python ${INSTALLDIR}/${REPO}/manage.py"

$manage migrate --noinput
$manage load_photosizes
$manage load_layers
$manage collectstatic --noinput
