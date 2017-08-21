from django.shortcuts import render


def index(request):
    return render(request, 'Index-recipe-search.html')

