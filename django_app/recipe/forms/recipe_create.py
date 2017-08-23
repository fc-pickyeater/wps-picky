from django import forms

from recipe.models import Recipe


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredient',
            'img_recipe',
        ]
