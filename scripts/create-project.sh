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

# We need these variations
APP_UPPER=`echo ${APP} | tr '[:lower:]' '[:upper:]'`
APP_UNDERSCORE=`echo ${APP} | sed -r 's/-/_/g'`
APP_UNDERSCORE_UPPER=`echo ${APP_UNDERSCORE} | tr '[:lower:]' '[:upper:]'`

# Create the project
PROJECT_DIR=${CREATE_DIR}/${APP}
APP_DIR=${PROJECT_DIR}/${APP_UNDERSCORE}
mkdir $PROJECT_DIR

# Copy requisite bits
cp .gitignore ${PROJECT_DIR}/
cp setup.py ${PROJECT_DIR}/
cp setup-development.sh ${PROJECT_DIR}/
cp manage.py ${PROJECT_DIR}/
cp MANIFEST.in ${PROJECT_DIR}/
cp tox.ini ${PROJECT_DIR}/
cp .travis.yml ${PROJECT_DIR}/
cp .babelrc ${PROJECT_DIR}/
cp .editorconfig ${PROJECT_DIR}/
cp .eslintrc ${PROJECT_DIR}/
cp .nvmrc ${PROJECT_DIR}/
cp package.json ${PROJECT_DIR}/
cp .stylelintrc ${PROJECT_DIR}/
cp webpack.config.js ${PROJECT_DIR}/
cp yarn.lock ${PROJECT_DIR}/
touch ${PROJECT_DIR}/AUTHORS.rst
touch ${PROJECT_DIR}/CHANGELOG.rst
touch ${PROJECT_DIR}/README.rst
cp -r project ${PROJECT_DIR}/
cp -r requirements ${PROJECT_DIR}/
cp -r mote ${PROJECT_DIR}/
cp -r build-helpers ${PROJECT_DIR}/
cp -r skeleton ${APP_DIR}

# Delete pyc files
find ${PROJECT_DIR} -name "*.pyc" | xargs rm

# Change strings in the newly copied source
sed -i s/name=\"mobius-skeleton\"/name=\"${APP}\"/ ${PROJECT_DIR}/setup.py

# Replace the word skeleton with the app name, taking care to exclude some files
find ${PROJECT_DIR} -type f -exec sed -i s/SKELETON/${APP_UNDERSCORE_UPPER}/g {} +
find ${PROJECT_DIR} -type f \( ! -iname "setup.py" \) -exec sed -i s/skeleton/${APP_UNDERSCORE}/g {} +

# Rename directories
mv ${APP_DIR}/templates/skeleton ${APP_DIR}/templates/${APP_UNDERSCORE}
mv ${APP_DIR}/static/skeleton ${APP_DIR}/static/${APP_UNDERSCORE}
mv ${PROJECT_DIR}/mote/projects/skeleton ${PROJECT_DIR}/mote/projects/${APP_UNDERSCORE}

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
