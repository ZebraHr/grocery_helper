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
                            #  FavoriteSerializer,
                             ShoppingCartSerializer,
                             FollowSerializer,
                             RecipeReadSerializer
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
            serializer = RecipeReadSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            fav_rec = Favorite.objects.filter(user=request.user, recipe__id=pk)
            if fav_rec.exists():
                fav_rec.delete()
                return Response(
                    {'message': 'Рецепт удален из избранного!'},
                    status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт уже удален!'},
                status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """Вьюсет для подписок.
       Просмотр, подписка на пользователя,
       удаление подписки."""
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('user__username', 'subscribing__username')

    def get_queryset(self):
        return self.request.user.subscriber.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def destroy(self, serializer):
    #     author = get_object_or_404(User, username=username)
    #     if author != self.request.user:
    #         return serializer.save(user=self.request.user)
    #     return Response('На себя подписка невозможна!',
    #                     status=status.HTTP_400_BAD_REQUEST)

    # # def delete(self, username):
    # #     author = get_object_or_404(User, username=username)
    # #     follower = Follow.objects.filter(user=self.request.user,
    # #                                      author=author)
    # #     if follower.exists():
    # #         return follower.delete()
                                                                                                                                                