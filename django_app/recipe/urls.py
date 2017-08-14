from django.conf.urls import url

from . import apis

urlpatterns = [
    # Recipe
    # 레시피의 기본내용 리스트 조회
    url(r'^$', apis.RecipeListView.as_view()),
    # 레시피 상세 조회 + 레시피 스텝
    url(r'^detail/(?P<pk>\d+)/$', apis.RecipeDetailView.as_view()),
    # 마이페이지
    url(r'^mylist/', apis.MyRecipeListView.as_view()),
    # 북마크
    url(r'^bookmark/$', apis.BookMarkListView.as_view()),
    url(r'^bookmark/(?P<recipe_pk>\d+)/$', apis.BookMarkView.as_view()),
    # 좋아요
    url(r'^like/(?P<recipe_pk>\d+)/$', apis.RecipeLikeView.as_view()),
    # 평점
    url(r'^rate/(?P<recipe_pk>\d+)/$',apis.RecipeRateView.as_view()),
    # recipe step
    # url(r'^step/$', apis.RecipeStepCreateView.as_view()),
    # recipestepcomment
    url(r'^step/comment/$', apis.RecipeStepCommentListView.as_view()),
    url(r'^step/(?P<pk>\d+)/comment/create/$', apis.RecipeStepCommentCreateView.as_view()),
    url(r'^step/comment/modify/(?P<pk>\d+)/$', apis.RecipeStepCommentModifyView.as_view()),  # 수정삭제
    url(r'^step/(?P<pk>\d+)/$', apis.RecipeStepModifyDeleteView.as_view()),
    # recipe search
    url(r'^search/$', apis.RecipeSearchListView.as_view()),

    # 레시피 생성
    url(r'^create/$', apis.RecipeCreateForFDS.as_view()),
    # 레시피 수정, 삭제. 테스트 필요 8/10 joe
    url(r'^update/(?P<pk>\d+)/$', apis.RecipeModifyDelete.as_view()),

    # RecipeReview
    # 레시피 리뷰 조회
    url(r'^(?P<pk>\d+)/review/$', apis.RecipeReviewListView.as_view()),
    # 레시피 리뷰 생성
    url(r'^(?P<pk>\d+)/review/create/$', apis.RecipeReviewCreateView.as_view()),
    # 레시피 리뷰 수정, 삭제
    url(r'^review/modify/(?P<pk>\d+)/$', apis.RecipeReviewModifyView.as_view()),

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
