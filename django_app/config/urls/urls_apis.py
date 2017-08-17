from django.conf.urls import include, url

urlpatterns = [
    # ingredient 매핑 - hong 8/1
    url(r'^ingredient/', include('ingredient.urls')),
    # recipe 매핑 - hong 8/1
    url(r'^recipe/', include('recipe.urls')),
    url(r'^member/', include('member.urls.urls_apis')),
]
