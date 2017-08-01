from django.conf.urls import url

from recipe import apis

urlpatterns =[
    # recipe/로 접근하면 생성가능한 url postman확인 - hong 8/1
    url(r'^$', apis.RecipeCreateView.as_view())
]