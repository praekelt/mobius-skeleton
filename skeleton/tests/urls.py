from django.conf.urls import include, patterns, url


urlpatterns = [
    url(r"^", include("project.urls")),
]
