from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (IngredientViewSet,
                       TagViewSet,
                       CustomUserViewSet,
                       RecipeViewSet,
                       )

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
# router.register('subscriptions', FollowViewSet, basename='subscription')
router.register('recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
