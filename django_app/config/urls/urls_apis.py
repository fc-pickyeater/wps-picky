from django.conf.urls import include, url

urlpatterns = [
    url(r'^ingredient/', include('ingredient.urls')),
    url(r'^recipe/',include('recipe.urls'))


]
