from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.RecipeListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),

    url(r'^mylist/', apis.MyRecipeListView.as_view()),
    url(r'^bookmark/$', apis.BookMarkListView.as_view()),
    url(r'^bookmark/(?P<recipe_pk>\d+)/$', apis.BookMarkView.as_view()),

    # recipe step
    # url(r'^step/$', apis.RecipeStepCreateView.as_view()),
    # recipestepcomment
    url(r'^step/comment/$', apis.RecipeStepCommentListView.as_view()),
    url(r'^step/(?P<pk>\d+)/comment/create/$', apis.RecipeStepCommentCreateView.as_view()),
    url(r'^step/comment/modify/(?P<pk>\d+)/$', apis.RecipeStepCommentModifyView.as_view()),  # 수정삭제
    url(r'^step/(?P<pk>\d+)/$', apis.RecipeStepModifyDeleteView.as_view()),
    # recipe search
    url(r'^search/$', apis.RecipeSearchListView.as_view()),
    url(r'^create/$', apis.RecipeCreateForFDS.as_view()),

    # recipe step
    # url(r'^step/$', apis.RecipeStepCreateView.as_view()),
    url(r'^step/create/$', apis.RecipeStepCreateForFDS.as_view()),
    url(r'^step/(?P<pk>\d+)/$', apis.RecipeStepModifyDeleteView.as_view()),

]
