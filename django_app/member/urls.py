from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.PickyUserList.as_view()),
    url(r'(?P<pk>\d+)/$', apis.PickyUserDetailUpdate.as_view()),
    url(r'(?P<pk>\d+)/delete/$', apis.PickyUserDelete.as_view()),
    url(r'^create/$', apis.PickyUserCreate.as_view()),
]