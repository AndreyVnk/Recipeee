from django.contrib import admin

from .models import Recipe, RecipeIngredient, Tag, TagRecipe, Ingredient, Favorite, ShoppingCart, Follow

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(RecipeIngredient)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Follow)