from django.conf.urls import url, include
from django.contrib import admin
from . import urls_apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(urls_apis)),
]



