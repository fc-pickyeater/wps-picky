from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login

from member.forms import LoginForm


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


