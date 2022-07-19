from django.contrib import admin

from .models import Recipe, RecipeIngredient, Tag, TagRecipe, Ingredient

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(RecipeIngredient)
