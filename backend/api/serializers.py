import base64

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorite,
                            ShoppingCart,
                            Follow)
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ''
        model = User


class IngredientSerializer(serializers.ModelSerializer):
    """Ингредиенты."""
    class Meta:
        fields = '__all__'
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Теги."""
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Favorite


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
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following', )
        model = Follow
        read_only_fields = ('owner',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
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
