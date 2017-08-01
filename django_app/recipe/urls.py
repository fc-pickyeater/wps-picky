from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeList.as_view()),
]