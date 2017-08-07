from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),
    # recipe step
    url(r'^step/$', apis.RecipeStepCreateView.as_view()),
    url(r'^step/(?P<pk>\d+)/$', apis.RecipeStepModifyView.as_view()),
    url(r'^step/comment/$', apis.RecipeStep_CommentListView.as_view()),
    url(r'^step/comment/create/$', apis.RecipeStep_CommentCreateView.as_view()),
]
