
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, blank=False)
    color = models.CharField(max_length=32, unique=True, blank=False)
    slug = models.SlugField(
        _('Tag slug'), unique=True, max_length=50, blank=False
    )

    class Meta:
        verbose_name = _('Tags')
        verbose_name_plural = _('Tags')
        ordering = ['slug']

    def __str__(self):
        return self.name    



class Ingredient(models.Model):
    name = models.CharField(_('Name'), max_length=200, blank=False)
    measurement_unit = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredient')

    def __str__(self):
        return self.name    


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Recipe author'),
    )
    name = models.CharField(_('Name'), max_length=200, blank=False)
    image = models.ImageField(
        'Image',
        upload_to='recipes/',
        null=True, blank=True
    )
    text = models.TextField(_('Describing'),)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag, through='TagRecipe',
        related_name='recipes'

    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = _('Recipes')
        verbose_name_plural = _('Recipes')
        ordering = ['name']

    def __str__(self):
        return self.name    
        

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Amount',
        validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ("recipe", "ingredient")


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("tag", "recipe")

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ("user", "author")

class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shopping_cart',)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shopping_cart',)

    class Meta:
        unique_together = ("user", "recipe")

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites',)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites',)

    class Meta:
        unique_together = ("user", "recipe")