from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers, serializers, viewsets
import rest_framework_extras
from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm
from jmbo import api as jmbo_api
from post import api as post_api
from listing import api as listing_api


router = routers.DefaultRouter()

rest_framework_extras.discover(router)
rest_framework_extras.register(router)

# Register jmbo suite routers
jmbo_api.register(router)
post_api.register(router)
listing_api.register(router)

admin.autodiscover()

urlpatterns = [
    url(r"^", include("skeleton.urls", namespace="skeleton")),
    url(r"^mobius/", include("mobius.urls", namespace="mobius")),
    url(r"^api/(?P<version>(v1))/", include(router.urls)),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^jmbo/", include("jmbo.urls", namespace="jmbo")),
    url(r"^post/", include("post.urls", namespace="post")),
    url(r"^link/", include("link.urls", namespace="link")),
    url(r"^listing/", include("listing.urls", namespace="listing")),
    url(r"^navbuilder/", include("navbuilder.urls", namespace="navbuilder")),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^api-auth/$", obtain_jwt_token, name="obtain_token"),
    url(r"^mote/", include("mote.urls", namespace="mote")),
    url(r"^auth/", include("django.contrib.auth.urls", namespace="auth")),
    # Comments can't handle namespaces
    url(r"^comments/", include("django_comments.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        url(
            r"^media/(?P<path>.*)$", "django.views.static.serve",
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True}
        ),
    ]
