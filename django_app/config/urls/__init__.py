from django.conf.urls import url, include

from . import urls_apis

urlpatterns = [
    url(r'', include(urls_apis)),
]
