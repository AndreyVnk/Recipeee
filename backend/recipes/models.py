
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    slug = models.SlugField(
        _('Tag slug'), unique=True, max_length=50, blank=False
    )

    def __str__(self):
        return self.name    

    class Meta:
        verbose_name = _('Tags')
        verbose_name_plural = _('Tags')
        ordering = ['slug']

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
    text = models.CharField(_('Describing'), max_length=300,)

    ingredient = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        related_name='ingredients'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    image = models.ImageField(
        'Image',
        upload_to='recipes/',
        null=True, blank=True
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        Tag, through='TagRecipe'

    )

    class Meta:
        verbose_name = _('Recipes')
        verbose_name_plural = _('Recipes')
        ordering = ['name']

    def __str__(self):
        return self.name    
        

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    amount = models.IntegerField(
        verbose_name='Amount',
        validators=[MinValueValidator(0)])


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'