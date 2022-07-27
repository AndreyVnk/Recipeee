from dataclasses import fields
from requests import delete
from rest_framework import serializers
from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, Favorite, ShoppingCart, TagRecipe
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from drf_extra_fields.fields import Base64ImageField
from users.serializers import UserSerializer
from rest_framework.validators import UniqueTogetherValidator

from django.shortcuts import get_object_or_404


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class AmountIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = AmountIngredientSerializer(
        read_only=True, many=True, source='recipeingredient_set'
    )
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'image', 'name', 'text', 'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {"Message": "Tags must be set"}
            )
        if not ingredients:
            raise serializers.ValidationError(
                {"Message": "Ingredients must be set"}
            )
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'This ingredient is in list'
                )
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': 'Amount must be more than 0'
                })
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(shopping_cart__user=user, id=obj.id).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            pk = ingredient['id']
            current_ingredient = Ingredient.objects.get(pk=pk)
            amount = ingredient['amount']
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={'amount': amount}
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.name)
        instance.image = validated_data.get('image', instance.name)
        instance.cooking_time = validated_data.get('cooking_time', instance.name)
        instance.tags.clear()
        tags = validated_data.get('tags')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredients')
        for ingredient in ingredients:
            pk = ingredient['id']
            current_ingredient = Ingredient.objects.get(pk=pk)
            amount = ingredient['amount']
            instance.ingredients.add(
                current_ingredient,
                through_defaults={'amount': amount}
            )
        instance.save()
        return instance


class MinRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')