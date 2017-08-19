from django.views.generic import DetailView, ListView

from recipe.models import Recipe


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeListView(ListView):
    model = Recipe


