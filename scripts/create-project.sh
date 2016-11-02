#! /bin/bash

# Will move to Genshi templates in future

# Defaults
CREATE_DIR=/tmp

# Prompt for params
echo -n "App name, eg. myapp. [enter]: "
read APP
echo -n "Source code directory. (default=/tmp) [enter]: "
read adir
if [ -n "$adir" ];
then
    CREATE_DIR=$adir
fi

# Create the project
PROJECT_DIR=${CREATE_DIR}/${APP}
APP_DIR=${PROJECT_DIR}/${APP}
mkdir $PROJECT_DIR

# Copy requisite bits
cp .gitignore ${PROJECT_DIR}/
cp setup.py ${PROJECT_DIR}/
cp setup-development.sh ${PROJECT_DIR}/
cp manage.py ${PROJECT_DIR}/
cp MANIFEST.in ${PROJECT_DIR}/
cp tox.ini ${PROJECT_DIR}/
cp .travis.yml ${PROJECT_DIR}/
touch ${PROJECT_DIR}/AUTHORS.rst
touch ${PROJECT_DIR}/CHANGELOG.rst
touch ${PROJECT_DIR}/README.rst
cp -r scripts ${PROJECT_DIR}/
cp -r project ${PROJECT_DIR}/
cp -r fed ${PROJECT_DIR}/
cp -r requirements ${PROJECT_DIR}/
cp -r skeleton ${PROJECT_DIR}/${APP}

# Delete pyc files
find ${PROJECT_DIR} -name "*.pyc" | xargs rm

# Change strings in the newly copied source
sed -i s/name=\'jmbo-skeleton\'/name=\'${APP}\'/ ${PROJECT_DIR}/setup.py

# Replace the word skeleton with the app name
sed -i s/skeleton/${APP}/g ${PROJECT_DIR}/*.py
sed -i s/skeleton/${APP}/g ${PROJECT_DIR}/project/*.py
sed -i s/skeleton/${APP}/g ${PROJECT_DIR}/MANIFEST.in
sed -i s/skeleton/${APP}/g ${PROJECT_DIR}/tox.ini
sed -i s/skeleton/${APP}/g ${PROJECT_DIR}/.travis.yml
APP_UPPER=`echo ${APP} | tr '[:lower:]' '[:upper:]'`
sed -i s/SKELETON/${APP_UPPER}/g ${PROJECT_DIR}/project/settings.py
sed -i s/skeleton/${APP}/g ${APP_DIR}/*.py
sed -i s/skeleton/${APP}/g ${APP_DIR}/migrations/*.py
sed -i s/skeleton/${APP}/g ${APP_DIR}/tests/settings/*.py

# Rename directories
mv ${APP_DIR}/templates/skeleton ${APP_DIR}/templates/${APP}
mv ${APP_DIR}/static/skeleton ${APP_DIR}/static/${APP}

# Set the secret key
SECRET_KEY=`date +%s | sha256sum | head -c 56`
sed -i "s/SECRET_KEY_PLACEHOLDER/${SECRET_KEY}/" ${PROJECT_DIR}/project/settings.py

# Indicate version of jmbo-skeleton used to create project
VERSION=`sed "5q;d" setup.py | awk -F= '{print $2}'`
echo "Changelog" > ${PROJECT_DIR}/CHANGELOG.rst
echo "=========" >> ${PROJECT_DIR}/CHANGELOG.rst
echo "" >> ${PROJECT_DIR}/CHANGELOG.rst
echo "0.1" >> ${PROJECT_DIR}/CHANGELOG.rst
echo "---" >> ${PROJECT_DIR}/CHANGELOG.rst
echo "Project generated by mobius-skeleton $VERSION" >> ${PROJECT_DIR}/CHANGELOG.rst
echo "" >> ${PROJECT_DIR}/CHANGELOG.rst

echo "Done."
