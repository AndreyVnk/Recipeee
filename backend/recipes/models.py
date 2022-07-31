from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Tag(models.Model):
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]

    name = models.CharField(
        _('Name'), max_length=32, unique=True, blank=False
        )
    color = models.CharField(
        _('Color'), max_length=32, unique=True, choices=COLOR_CHOICES,
    )
    slug = models.SlugField(
        _('Tag slug'), unique=True, max_length=50, blank=False
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(_('Name'), max_length=200, blank=False)
    measurement_unit = models.CharField(
        _('Measurement_unit'), max_length=15)

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredient')
        constraints = [
            models.UniqueConstraint(fields=('name', 'measurement_unit',),
                                    name='unique ingredient')
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        _('Recipe author'),
        CustomUser,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_('Name'), max_length=200, blank=False)
    image = models.ImageField(
        _('Image'),
        upload_to='recipes/',
        null=True, blank=True
    )
    text = models.TextField(_('Describing'),)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes'

    )
    cooking_time = models.IntegerField(
        _('Cooking_time'),
        validators=[
            MinValueValidator(1)
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Recipes')
        verbose_name_plural = _('Recipes')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        _('Ingredient'),
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        _('Recipe'),
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        _('Amount'),
        validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Igredient amount'
        verbose_name_plural = 'Igredient amounts'
        unique_together = ("recipe", "ingredient")


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        _('Tag'),
        Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        _('Recipe'),
        Recipe, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)
        unique_together = ("tag", "recipe")

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        _('User'),
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        _('Recipe'),
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'
        unique_together = ("user", "recipe")


class Favorite(models.Model):
    user = models.ForeignKey(
        _('User'),
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        _('Recipe'),
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        unique_together = ("user", "recipe")
