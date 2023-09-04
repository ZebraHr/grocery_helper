from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (IngredientViewSet,
                       TagViewSet,
                       FollowViewSet,
                       )

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('ingredients', IngredientViewSet)
v1_router.register('tags', TagViewSet)
v1_router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
