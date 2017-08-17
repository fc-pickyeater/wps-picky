from django.conf.urls import url

from .apis.auth import obtain_auth_token, FacebookLoginAPIView
from . import apis

urlpatterns = [
    url(r'^$', apis.PickyUserList.as_view()),
    url(r'^create/$', apis.PickyUserCreate.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', apis.PickyUserDetail.as_view()),
    url(r'^update/(?P<pk>\d+)/$', apis.PickyUserUpdate.as_view()),
    # url(r'^delete/(?P<pk>\d+)/$', apis.PickyUserDelete.as_view()),
    # 로그인시, 토큰을 생성하는 url
    url(r'^login/$', obtain_auth_token),
    url(r'^facebook-login/$', FacebookLoginAPIView.as_view()),
    url(r'^logout/$', apis.PickyUserLogout.as_view()),
]
