from django.shortcuts import render
from django.views.generic import ListView

from .models import Recipe

# def index(request):
#     return render(request, 'recipes/indexNotAuth.html', context={})


class Index(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/indexNotAuth.html'