from django.conf.urls import url

from recipe import views

app_name = 'recipe'
urlpatterns = [
    url(r'^$', views.RecipeListView.as_view(), name='recipe_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.RecipeDetailView.as_view(), name='recipe_detail'),
    url(r'^search/$', views.recipe_search, name='search'),

    # url(r'^create/$', apis.PickyUserCreate.as_view()),
    #
    # url(r'^update/(?P<pk>\d+)/$', apis.PickyUserUpdate.as_view()),
    # # url(r'^delete/(?P<pk>\d+)/$', apis.PickyUserDelete.as_view()),
    # # 로그인시, 토큰을 생성하는 url
    # url(r'^login/$', obtain_auth_token),
    # url(r'^facebook-login/$', FacebookLoginAPIView.as_view()),
    # url(r'^logout/(?P<pk>\d+)$', apis.PickyUserLogout.as_view()),
]
