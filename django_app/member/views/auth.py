from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout

from member.forms import LoginForm
from member.forms.signup import SignupForm


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'member/pickyuser_login.html', context)
    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            return redirect('recipe:search')


def logout(request):
    django_logout(request)
    return redirect('recipe:search')


def signup(request):
    if request.method == 'GET':
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, 'member/pickyuser_signup.html', context)
    elif request.method == 'POST':
        form = SignupForm(
                data=request.POST,
                files=request.FILES,
        )
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect('recipe:search')


