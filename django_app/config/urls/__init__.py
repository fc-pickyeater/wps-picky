from django.conf.urls import url, include
from . import urls_apis
from django.contrib import admin

urlpatterns = [
    url(r'', include(urls_apis)),
url(r'^admin/', admin.site.urls),
]
