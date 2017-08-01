from django.conf.urls import url

from recipe import apis

urlpatterns =[
    url(r'^$', apis.RecipeCreateView.as_view())
]