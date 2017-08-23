from django.conf.urls import url

from recipe import views

app_name = 'recipe'
urlpatterns = [
    url(r'^$', views.RecipeListView.as_view(), name='recipe_list'),
    url(r'^detail/(?P<pk>\d+)/$', views.RecipeDetailView.as_view(), name='recipe_detail'),
    url(r'^search/$', views.recipe_search, name='search'),
    url(r'^create/$', views.RecipeCreateView.as_view(), name='recipe_create'),
    # url(r'^step/create/$', views.RecipeStepCreateView.as_view(), name='recipestep_create'),

]
