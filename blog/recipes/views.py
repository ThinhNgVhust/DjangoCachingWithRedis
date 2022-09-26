from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,View
from .models import Category,Recipe

from django.core.cache import cache

# Create your views here.


class RecipesView(ListView):
    queryset = Recipe.objects.all()
    context_object_name = "recipes"
    template_name = "recipes/recipes.html"

class RecipeView(ListView):
    def get(self,request,*args,**kwargs):
        recipe_id = kwargs["pk"]
        mess = ""
        if cache.get(recipe_id):
            recipe = cache.get(recipe_id)
            mess = ("hit the cache")
        else:
            try:
                recipe = Recipe.objects.get(pk=recipe_id)
                cache.set(recipe_id,recipe)
            except Recipe.DoesNotExist:
                return HttpResponse("This recipe does not exist.")
            mess = ("hit the db and save cache")
        context = {"recipe":recipe}
        return HttpResponse(mess)