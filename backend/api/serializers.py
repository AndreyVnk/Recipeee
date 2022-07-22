from rest_framework import serializers
from recipes.models import Tag, Recipe, TagRecipe, Ingredient
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(validators=[
        UniqueValidator(queryset=Tag.objects.all()),
        RegexValidator(regex='^[-a-zA-Z0-9_]+$')
    ])

    class Meta:
        model = Tag
        fields = ('id', 'name',' color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=False)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        if 'tags' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag)
            TagRecipe.objects.create(
                name=current_tag, recipe=recipe)
        return recipe