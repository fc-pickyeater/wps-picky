from django.conf.urls import include, url

urlpatterns = [
    # django templates 작업용
    # url(r'^%', include('ingredient.urls')),
    url(r'^recipe/', include('recipe.urls.urls_views')),
    url(r'^member/', include('member.urls.urls_views')),
]
