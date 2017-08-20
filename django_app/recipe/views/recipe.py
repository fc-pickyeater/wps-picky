from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.utils.encoding import force_text
from django.views.generic import DetailView, ListView

from recipe.models import Recipe


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeListView(ListView):
    model = Recipe
