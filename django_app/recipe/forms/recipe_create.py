from django import forms
from django.forms import BaseModelFormSet, modelformset_factory

from recipe.models import Recipe, RecipeStep


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredient',
            'img_recipe',
        ]


class RecipeStepCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = '__all__'

