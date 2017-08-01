from django.conf.urls import url

from . import apis

urlpatterns = [
    url(r'^$', apis.IngredientSearchList.as_view()),
    url(r'(?P<pk>\d+)/$', apis.IngredientModifyDelete.as_view()),
]
