from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.PickyUserList.as_view()),
    url(r'(?P<pk>\d+)/$', apis.PickyUserDetail.as_view()),
    url(r'^create/$', apis.PickyUserCreate.as_view()),
]