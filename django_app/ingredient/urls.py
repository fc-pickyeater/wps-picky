from django.conf.urls import url

from . import apis

urlpatterns = [
    # ingredient/로 접근 get요청시 list,?name= 검색어 하면 검색가능 postman확인 - hong 8/1
    url(r'^$', apis.IngredientSearchListCreateView.as_view()),
    # ingredient/pk/로 접근 post시 생성 patch시 수정 delete시 삭제 postman확인 - hong 8/1
    url(r'^(?P<pk>\d+)/$', apis.IngredientModifyDeleteView.as_view()),
]
