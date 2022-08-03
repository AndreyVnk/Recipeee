from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Tag(models.Model):
    """Tag model."""

    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, _('Blue')),
        (ORANGE, _('Orange')),
        (GREEN, _('Green')),
        (PURPLE, _('Purple')),
        (YELLOW, _('Yellow')),
    ]

    name = models.CharField(_('Name'), max_length=32, unique=True)
    color = models.CharField(
        _('Color'), max_length=32, unique=True, choices=COLOR_CHOICES,
    )
    slug = models.SlugField(_('Tag slug'), unique=True, max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model."""

    name = models.CharField(_('Name'), max_length=200)
    measurement_unit = models.CharField(
        _('Measurement_unit'), max_length=15)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')
        constraints = [
            models.UniqueConstraint(fields=('name', 'measurement_unit',),
                                    name='unique ingredient')
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model."""

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_('Name'), max_length=200)
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
    pub_date = models.DateTimeField(
        _('Public date'), auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """RecipeIngredient model."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        _('Amount'),
        validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _('Igredient amount')
        verbose_name_plural = _('Igredient amounts')
        constraints = [
            models.UniqueConstraint(fields=('ingredient', 'recipe',),
                                    name='unique recipe ingredients')
        ]


class TagRecipe(models.Model):
    """TagRecipe model."""

    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        related_name='tags'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='tags'
    )

    class Meta:
        verbose_name = _('Tag recipe')
        verbose_name_plural = _('Tag recipes')
        constraints = [
            models.UniqueConstraint(fields=('tag', 'recipe',),
                                    name='unique recipe tags')
        ]

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class ShoppingCart(models.Model):
    """ShoppingCart model."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Shopping cart')
        verbose_name_plural = _('Shopping carts')
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe',),
                                    name='unique shopping cart')
        ]


class Favorite(models.Model):
    """Favorite model."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe',),
                                    name='unique favorite')
        ]
