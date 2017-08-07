from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from . import apis

urlpatterns = [
    url(r'^$', apis.PickyUserList.as_view()),
    url(r'(?P<pk>\d+)/$', apis.PickyUserDetailUpdate.as_view()),
    url(r'(?P<pk>\d+)/delete/$', apis.PickyUserDelete.as_view()),
    url(r'^create/$', apis.PickyUserCreate.as_view()),
    # url(r'^login/$', apis.PickyUserLogin.as_view()),
    # 로그인시, 토큰을 생성하는 url
    url(r'^login/$', obtain_auth_token),
]
