from django.conf.urls import include, url

urlpatterns = [
    url(r'^ingredient/', include('ingredient.urls')),


]
