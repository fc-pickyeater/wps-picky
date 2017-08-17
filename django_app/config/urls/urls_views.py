from django.conf.urls import include, url

urlpatterns = [
    # django templates 작업용
    url(r'^ingredient/', include('ingredient.urls')),
    url(r'^recipe/', include('recipe.urls')),
    url(r'^member/', include('member.urls.urls_views')),
]
