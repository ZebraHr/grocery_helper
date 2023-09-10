from rest_framework import viewsets, status, exceptions
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated,
                                        AllowAny,
                                        SAFE_METHODS)
from rest_framework import filters
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework.decorators import action

from api.serializers import (UserCreateSerializer,
                             UserReadSerializer,
                             IngredientSerializer,
                             TagSerializer,
                             RecipeCreateSerializer,
                             ShoppingCartSerializer,
                             RecipeReadSerializer,
                             SubscribeSerializer,
                             SubscriptionsSerializer,
                             )
from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorite,
                            ShoppingCart,
                            Subscribe)
from users.models import User
from api.permissions import (IsOwnerOrReadOnly,
                             IsAmdinOrReadOnly)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для просмотра профиля и создания пользователя."""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserReadSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ],
        url_path='subscribe'
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            if user == author:
                return Response({'errors': 'На себя подписаться нельзя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(user=user,
                                        author=author).exists():
                return Response({'errors': 'Вы уже подписаны на этого пользователя!'},
                                status=status.HTTP_400_BAD_REQUEST)

            Subscribe.objects.create(user=user, author=author)
            serializer = SubscribeSerializer(author,
                                             context={'request': request}
                                             )
          
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = Subscribe.objects.filter(user=user, author=author)
            if subscription.exists():
                subscription.delete()
                return Response(
                    {'message': 'Вы больше не подписаны на пользователя'},
                    status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST)

    # @action(
    #     detail=True,
    #     permission_classes=[IsAuthenticated, ]
    # )
    # def subscriptions(self, request):
    #     user = request.user
    #     queryset = User.objects.filter(subscribing__user=user)
    #     pages = self.paginate_queryset(queryset)
    #     serializer = SubscriptionsSerializer(pages,
    #                                      many=True,
    #                                      context={'request': request})
    #     return self.get_paginated_response(serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для просмотра ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAmdinOrReadOnly]


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для просмотра тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAmdinOrReadOnly]


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецепта.
       Просмотр, создание, редактирование."""
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user,
                                       recipe__id=pk).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeReadSerializer(recipe,
                                              context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            fav_rec = Favorite.objects.filter(user=request.user, recipe__id=pk)
            if fav_rec.exists():
                fav_rec.delete()
                return Response(
                    {'message': 'Рецепт удален из избранного'},
                    status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт уже удален!'},
                status=status.HTTP_400_BAD_REQUEST)
