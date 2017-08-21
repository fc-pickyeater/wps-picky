from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

PickyUser = get_user_model()


class SignupForm(UserCreationForm):
    img_profile = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        model = PickyUser
        fields = ('email', 'nickname', 'password1', 'password2', 'content',)
        field_classes = {'email': UsernameField}

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        print(user)
        print(self.cleaned_data['img_profile'])
        user.img_profile = self.cleaned_data['img_profile']
        if commit:
            user.save()
        return user


