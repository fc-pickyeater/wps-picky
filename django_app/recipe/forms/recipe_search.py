from django import forms


class RecipeSearchForm(forms.Form):
    search = forms.CharField(label=None, max_length=100)
