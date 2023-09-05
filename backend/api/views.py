from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework import filters
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from api.serializers import (UserSerializer,
                             IngredientSerializer,
                             TagSerializer,
                             RecipeSerializer,
                             FavoriteSerializer,
                             ShoppingCartSerializer,
                             FollowSerializer
                             )
from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorite,
                            ShoppingCart,
                            Follow)
from users.models import User
from api.permissions import (IsOwnerOrReadOnly,
                             IsAmdinOrReadOnly)


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
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для подписок.
       Просмотр, подписка на пользователя,
       удаление подписки."""
    serializer_class = FollowSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('user__username', 'following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, username, serializer):
        author = get_object_or_404(User, username=username)
        if author != self.request.user:
            return serializer.save(user=self.request.user)
        return Response('На себя подписка невозможна!',
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, username):
        author = get_object_or_404(User, username=username)
        follower = Follow.objects.filter(user=self.request.user,
                                         author=author)
        if follower.exists():
            return follower.delete()


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для добавления рецепта в избранное."""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_create(self):
    #     user = self.request.user
    #     fav_recipe = get_object_or_404(
    #         Recipe, pk=id)
    #     if Favorite.objects.filter(
    #             user=user,
    #             recipe=fav_recipe).exists():
    #         return Response('Рецепт уже в избранном!',
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         Favorite.objects.create(user=user, recipe=fav_recipe)

    def delete(self):
        user = self.request.user
        fav_recipe = get_object_or_404(
            Recipe, pk=id)
        if not Favorite.objects.filter(
                user=user,
                recipe=fav_recipe).exists():
            return Response('Рецепт нет в избранном!',
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return fav_recipe.delete()
