from import_export import resources
from recipes.models import Ingredient, Tag


class RecipesIngredient(resources.ModelResource):
    class Meta:
        model = Ingredient


class RecipesTag(resources.ModelResource):
    class Meta:
        model = Tag
