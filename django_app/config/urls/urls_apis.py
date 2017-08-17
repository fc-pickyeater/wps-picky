from django.conf.urls import include, url

urlpatterns = [
    # ingredient 매핑 - hong 8/1
    url(r'^api/ingredient/', include('ingredient.urls')),
    # recipe 매핑 - hong 8/1
    url(r'^api/recipe/', include('recipe.urls')),
    url(r'^api/member/', include('member.urls')),
]
