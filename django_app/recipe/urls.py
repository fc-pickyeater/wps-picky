from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),
    url(r'^create/$', apis.RecipeCreateForFDS.as_view()),

    # recipe step
    url(r'^step/$', apis.RecipeStepCreateView.as_view()),
    url(r'^step/create/$', apis.RecipeStepCreateForFDS.as_view()),
    url(r'^step/(?P<pk>\d+)/$', apis.RecipeStepModifyDeleteView.as_view()),

]
