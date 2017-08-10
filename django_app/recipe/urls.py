from django.conf.urls import url

from . import apis

urlpatterns = [
    # Recipe
    # 레시피의 기본내용 리스트 조회
    url(r'^$', apis.RecipeListView.as_view()),
    # 레시피 상세 조회 + 레시피 스텝
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),
    # 레시피 생성
    url(r'^create/$', apis.RecipeCreateForFDS.as_view()),
    # 레시피 수정, 삭제. 테스트 필요 8/10 joe
    url(r'^update/(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),

    # Recipe Step
    # 레시피 스텝 생성 (레시피 pk 필요)
    url(r'^step/create/$', apis.RecipeStepCreateForFDS.as_view()),
    # 레시피 스텝 수정, 삭제. 테스트 필요 8/10 joe
    url(r'^step/(?P<pk>\d+)/$', apis.RecipeStepModifyDeleteView.as_view()),

    # Recipe Step Comment
    # 레시피 스탭에 달려있는 코멘트 리스트 조회
    url(r'^step/comment/$', apis.RecipeStepCommentListView.as_view()),
    # 레시피 스텝에 코멘트를 작성
    url(r'^step/(?P<pk>\d+)/comment/create/$', apis.RecipeStepCommentCreateView.as_view()),
    # 레시피 스탭 코멘트를 수정,삭제
    url(r'^step/comment/modify/(?P<pk>\d+)/$', apis.RecipeStepCommentModifyView.as_view()),  # 수정삭제

    # Recipe Search
    url(r'^search/$', apis.RecipeSearchListView.as_view()),
]
