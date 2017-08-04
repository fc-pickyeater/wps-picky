from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeList.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    # recipe step
    url(r'^step_create/$', apis.RecipestepCreateView.as_view()),
    url(r'^step/(?P<pk>\d+)/$', apis.RecipestepModifyView.as_view())
]
