import base64

import webcolors
from django.core.files.base import ContentFile
from djoser.serializers import (PasswordSerializer, UserCreateSerializer,
                                UserSerializer)
from rest_framework import serializers, exceptions
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import IntegerField

from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorite,
                            ShoppingCart,
                            Subscribe,
                            IngredientAmount)
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserCreateSerializer(UserCreateSerializer):
    """Создание пользователя с обязательными полями."""
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserReadSerializer(UserSerializer):
    """Страница пользователя."""
    is_subscribed = serializers.SerializerMethodField

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', )

    def get_is_subcribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=request.user, author=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиенты в рецепте."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Игредиенты в рецепте."""
    id = serializers.ReadOnlyField(
        source='ingredient.id',
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Теги."""
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    author = SlugRelatedField(slug_field='username', read_only=True)
    ingredients = IngredientInRecipeWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField()

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Добавьте ингредиент.'
            )

        ingredients = [item['id'] for item in value]  # посмотреть и переписать
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    'Такой ингредиент уже добавлен.'
                )

        return value

    class Meta:
        model = Recipe
        exclude = ('pub_date',)


# class FavoriteSerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = '__all__'
#         model = Favorite


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShoppingCart


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'author', )
        model = Subscribe
 #       read_only_fields = ('owner',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Follow.objects.all(),
        #         fields=('user', 'author')
        #     )
        # ]

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise serializers.ValidationError(
                'Подписка на самого себя невозможна!'
            )
        return data


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class RecipeReadSerializer(serializers.ModelSerializer):
    """Просмотр рецепта."""
    tags = TagSerializer(
        many=True,
        # source='recipe_in_tags'
    )
    ingredients = IngredientsInRecipeSerializer(
        many=True,
        source='recipe'
    )
    author = UserReadSerializer()
    is_favorited = serializers.SerializerMethodField
    is_in_shopping_cart = serializers.SerializerMethodField

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj,
                                       user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()

# class SubscribeSerializer(serializers.ModelSerializer):
#     email = serializers.CharField(
#         source='author.email',
#         read_only=True)
#     id = serializers.IntegerField(
#         source='author.id',
#         read_only=True)
#     username = serializers.CharField(
#         source='author.username',
#         read_only=True)
#     first_name = serializers.CharField(
#         source='author.first_name',
#         read_only=True)
#     last_name = serializers.CharField(
#         source='author.last_name',
#         read_only=True)
#     recipes = serializers.SerializerMethodField()
#     is_subscribed = serializers.SerializerMethodField()
#     recipes_count = serializers.ReadOnlyField(
#         source='author.recipe.count')

#     class Meta:
#         model = Follow


