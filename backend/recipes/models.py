
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class Tag(models.Models):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name    


class Ingredient(models.Models):
    name = models.CharField(_('Название'), max_length=200, blank=False)
    measurement_unit = models.CharField(max_length=30, default='кг')
    
    class Meta:
        verbose_name = _('Ингридиент')
        verbose_name_plural = _('Ингридиент')


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Автор рецепта'),
    )
    name = models.CharField(_('Название'), max_length=200, blank=False)
    text = models.CharField(_('Описание'),)

    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    image = models.ImageField()
    tags = models.ManyToManyField(
        Tag, through='TagRecipe'

    )

    class Meta:
        verbose_name = _('Рецепты')
        verbose_name_plural = _('Рецепты')
        ordering = ['name']


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
        verbose_name='Количество',
        validators=[MinValueValidator(0)])


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'