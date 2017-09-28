from django.conf.urls import url


from ..apis.auth import FacebookLoginAPIView, obtain_auth_token
from .. import apis

urlpatterns = [
    url(r'^$', apis.PickyUserList.as_view()),
    url(r'^create/$', apis.PickyUserCreate.as_view()),
    url(r'^detail/(?P<pk>\d+)/$', apis.PickyUserDetail.as_view()),
    url(r'^update/(?P<pk>\d+)/$', apis.PickyUserUpdate.as_view()),
    # 로그인시, 토큰을 생성하는 url
    url(r'^login/$', obtain_auth_token),
    url(r'^facebook-login/$', FacebookLoginAPIView.as_view()),
    # url(r'^kakao-login/$', FacebookLoginAPIView.as_view()),
    url(r'^logout/$', apis.PickyUserLogout.as_view()),
    url(r'^password-reset/request/$', apis.PickyUserFindPassword.as_view()),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', apis.PickUserPasswordConfirm.as_view(), name='password-reset-confirm'),
    # url(r'^password-reset/done/$', apis.PickUserPasswordConfirm.as_view()),
]
