from django.core.paginator import InvalidPage, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import BaseCreateView

from recipe.forms import RecipeCreateForm
from recipe.models import Recipe, RecipeStep


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeListView(ListView):
    model = Recipe


class RecipeCreateView(CreateView):
    model = Recipe
    # fields = [
    #     'title',
    #     'description',
    #     'ingredient',
    #     'img_recipe',
    #
    # ]
    success_url = '/api/views/recipe/step/create/'
    form_class = RecipeCreateForm

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # 임시로 레시피 리스트로 이동
        return redirect('recipe:recipe_list')


# class RecipeStepCreateView(CreateView):
#     model = RecipeStep
#     fields = [
#         'description',
#         'img_step',
#         'is_timer',
#         'timer',
#         'recipe_id',
#     ]
