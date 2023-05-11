from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, Tag, ShoppingСart)
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = '__all__',


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAddAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_recipe',
        read_only=True, many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'name',
            'author',
            'ingredients',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

        def get_ingredients(self, obj):
            queryset = IngredientInRecipe.objects.filter(recipe=obj)
            return IngredientInRecipeSerializer(queryset, many=True).data

        def get_is_favorited(self, obj):
            request = self.context.get('request')
            if not request or request.user.is_anonymous:
                return False
            return Favorite.objects.filter(
                user=request.user, recipe=obj).exists()

        def get_is_in_shopping_cart(self, obj):
            request = self.context.get('request')
            if not request or request.user.is_anonymous:
                return False
            return ShoppingСart.objects.filter(
                user=request.user, recipe=obj).exists()


class AddRecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientAddAmountSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time')

        def validate_ingredients(self, data):
            ingredients = data['ingredients']
            if not ingredients:
                raise serializers.ValidationError(
                    'Поле ингредиентов не может быть пустым!')
            ingredients_list = []
            for ingredient in ingredients:
                ingredient_id = ingredient['id']
                if ingredient_id in ingredients_list:
                    raise serializers.ValidationError(
                        'В рецепте не может быть повторяющихся ингредиентов')
                ingredients_list.append(ingredient_id)
                amount = ingredient['amount']
                if int(amount) <= 0:
                    raise serializers.ValidationError(
                        'Число игредиентов должно быть больше 0')
            return data

        def validate_cooking_time(self, data):
            if data <= 0:
                raise serializers.ValidationError(
                        'Время приготовления должно быть больше 0!')
            return data

        def validate_tags(self, data):
            tags = data['tags']
            if not tags:
                raise serializers.ValidationError(
                    'Поле тэгов не может быть пустым!')
            return data

        @staticmethod
        def create_ingredients(ingredients, recipe):
            for ingredient in ingredients:
                IngredientInRecipe.objects.create(
                    recipe=recipe, ingredient=ingredient['id'],
                    amount=ingredient['amount'])

        @staticmethod
        def create_tags(tags, recipe):
            for tag in tags:
                recipe.tags.add(tag)

        def create(self, validated_data):
            author = self.context.get('request').user
            tags = validated_data.pop('tags')
            ingredients = validated_data.pop('ingredients')
            recipe = Recipe.objects.create(author=author, **validated_data)
            self.create_tags(tags, recipe)
            self.create_ingredients(ingredients, recipe)
            return recipe

        def to_representation(self, instance):
            request = self.context.get('request')
            context = {'request': request}
            return RecipeSerializer(instance, context=context).data

        def update(self, instance, validated_data):
            instance.tags.clear()
            IngredientInRecipe.objects.filter(recipe=instance).delete()
            self.create_tags(validated_data.pop('tags'), instance)
            self.create_ingredients(
                validated_data.pop('ingredients'), instance)
            return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
