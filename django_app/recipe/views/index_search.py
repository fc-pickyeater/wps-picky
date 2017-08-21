from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from recipe.forms.recipe_search import RecipeSearchForm
from recipe.models import Recipe


def recipe_search(request):
    if request.method == 'GET':
        form = RecipeSearchForm()
        print(form)
        context = {
            'form': form,
        }
        return render(request, 'Index-recipe-search.html', context=context)

    elif request.method == 'POST':
        form = RecipeSearchForm(request.POST)
        search = request.POST.get('search')
        if form.is_valid():
            recipe_id = list()
            search_result = Recipe.objects.filter(
                    Q(title__contains=search)|
                    Q(ingredient__contains=search)|
                    Q(recipetag__tag__content__contains=search)
            )
            if search_result:
                for recipe in search_result:
                    recipe_id.append(recipe.id)
                result = Recipe.objects.filter(pk__in=recipe_id)
                context = {
                    'recipe_list': result,
                }
                return render(request, 'recipe/recipe_list.html', context)
            return HttpResponse('검색 결과가 없습니다.')
