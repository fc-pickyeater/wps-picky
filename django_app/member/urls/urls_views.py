from django.conf.urls import url

from member import views

urlpatterns = [
    url(r'^$', views.PickyUserListView.as_view(), name='user_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.PickyUserDetailView.as_view(), name='user_detail'),

    # url(r'^create/$', apis.PickyUserCreate.as_view()),
    #
    # url(r'^update/(?P<pk>\d+)/$', apis.PickyUserUpdate.as_view()),
    # # url(r'^delete/(?P<pk>\d+)/$', apis.PickyUserDelete.as_view()),
    # # 로그인시, 토큰을 생성하는 url
    # url(r'^login/$', obtain_auth_token),
    # url(r'^facebook-login/$', FacebookLoginAPIView.as_view()),
    # url(r'^logout/(?P<pk>\d+)$', apis.PickyUserLogout.as_view()),
]
