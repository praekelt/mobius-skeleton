Changelog
=========

next
----
#. Deprecate buildout in favour of pip.
#. Move settings into a projects directory to avoid clutter.
#. Minimum supported version of `jmbo-foundry` is now 2.0.

0.9
---
#. Deprecate haproxy since a load balancer at another point in the chain does a better job.

0.8
---
#. `setup-server.sh` gets optional arguments for a leaner install.
#. `deploy-project.sh` does not lead to downtime anymore.
#. Haproxy config does not need both basic and smart backends for mobi anymore.
#. Remove media-links from configs. It is redundant.
#. Use gunicorn in way advised by Django.
#. Install `device-proxy` through pip from pypi.
#. Admin runs on its own instance. This enables us to set longer timeouts to handle the more expensive queries.
#. Mobile browsers are automatically directed to mobi now. They have the option of requesting the desktop site.

0.7.1
-----
#. Bump `jmbo-foundry` to 1.1.10.
#. Bump `jmbo-downloads` to 0.0.5.
#. Fix bug in `deploy-script.sh`.

0.7
---
#. Up `jmbo-foundry` to 1.1.9.
#. Media directories are now prefixed with the app name. This allows multiple Jmbo projects to live on the same server.
#. Simplify `create-jmbo-project.sh` by removing an option.
#. Force buildout 1.7.0 since version 2 has backward incompatible changes.

0.6
---
#. `device-proxy` and haproxy is now part of our setup. This enables user-agent to backend mapping.
#. Buildouts massively refactored. Everything can be regenerated using `create-project.sh`. `STATIC_URL` changes for basic and smart layers.

0.5.2
-----
#. `south` lowercase pin added.
#. `deploy-project.sh` now creates necessary cron entries.
#. Sentry is now part of our setup.

0.5.1
-----
#. `setup-development.sh` makes getting a development environment running easy.

0.5
---
#. Demo now uses location aware SQLite database.
#. versions.cfg is updated from this version onwards.
#. Up jmbo-foundry to 1.0, and jmbo to 1.0 since we now use a location aware database by default.

0.4.4
-----
#. Up jmbo-foundry to 0.7.2.
#. There are now four sites since page layouts may differ between eg. basic and smart.

0.4.3
-----
#. Up django-setuptest to 0.1.2.
#. Up jmbo-foundry to 0.7.1.
#. Copy .gitignore when creating a new project.

0.4.1
-----
#. Webdav access now enabled. It is useful for changing CSS on QA sites on the fly.
#. Webdav requires we backup static resources on each deploy. Added to deploy_project.sh.
#. Removed Praekelt assumption from deploy script.
#. Up required jmbo-foundry to 0.6.3. Django 1.4 is now implicitly required.
#. Up djangorecipe to 1.2.1 and handle case where Django name is suddenly case-sensitive when pinning.

0.4
---
#. Up minimum jmbo-foundry to 0.5.
#. Create a trivial south migration so order of migrations is correct.

0.3.2
-----
#. Dev buildout now uses git instead of https.

0.3.1
-----
#. Remove flup since it is currently broken. 
#. Create different sites for mobi and web.

0.3
---
#. Templates for mid and smart layers.
#. Server setup bug fixes.

0.2.4
-----
#. Fix manifest and up minimum jmbo-foundry to 0.4.

0.2.2
-----
#. Fix typos.

0.2.1
-----
#. Change egg name to jmbo-skeleton.

0.1
---
#. Initial release

