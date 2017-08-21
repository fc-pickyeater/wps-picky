from django.conf.urls import url

from member import views
from member.views import login, logout

app_name = 'member'
urlpatterns = [
    url(r'^$', views.PickyUserListView.as_view(), name='user_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.PickyUserDetailView.as_view(), name='user_detail'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    # url(r'^create/$', apis.PickyUserCreate.as_view()),
    #
    # url(r'^update/(?P<pk>\d+)/$', apis.PickyUserUpdate.as_view()),
    # # url(r'^delete/(?P<pk>\d+)/$', apis.PickyUserDelete.as_view()),
    # url(r'^facebook-login/$', FacebookLoginAPIView.as_view()),

]
