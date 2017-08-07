from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),
    # recipe step
    url(r'^step/$', apis.RecipestepCreateView.as_view()),
    url(r'^step/(?P<pk>\d+)/$', apis.RecipestepModifyView.as_view())
]
