from django.conf.urls import url

from recipe import apis
from . import apis as myapis

urlpatterns = [
    url(r'^recipe/$', myapis.MyRecipeListView.as_view()),
    url(r'^recipe/create/$', apis.RecipeCreateForFDS.as_view()),
    url(r'^recipe/(?P<PK>\d+)/$', apis.RecipeModifyDelete.as_view()),
]
