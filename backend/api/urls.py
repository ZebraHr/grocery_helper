from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (IngredientViewSet,
                       TagViewSet,
                       FollowViewSet,
                       RecipeViewSet,
                       FavoriteViewSet
                       )

app_name = 'api'

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('subscriptions', FollowViewSet, basename='subscription')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]
