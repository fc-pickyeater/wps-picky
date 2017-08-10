from django.conf.urls import url

from . import apis

urlpatterns = [
    # 레시피의 기본내용 리스트 조회
    url(r'^$', apis.RecipeListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),
    # 1개의 레시피와 레시피에 달려있는 레시피 스탭들을 보기위한
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),
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
