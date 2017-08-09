from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from member import views
from . import urls_apis
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'', include(urls_apis)),
]
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
    )
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
