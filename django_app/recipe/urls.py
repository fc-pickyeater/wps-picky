from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeList.as_view()),
    url(r'(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    url(r'^$', apis.RecipeCreateView.as_view()),
]