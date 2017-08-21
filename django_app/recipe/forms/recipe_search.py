from django import forms


class RecipeSearchForm(forms.Form):
    search = forms.CharField(
            label='',
            max_length=100,
            widget=forms.TextInput(
                    attrs={
                        'placeholder': '검색어를 입력하세요.',
                        'class': 'form-control',
                        # 'width': '80%'
                    }
            )
    )
