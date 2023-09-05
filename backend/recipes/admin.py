from django.contrib import admin

from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorite,
                            ShoppingCart,
                            Follow
                            )
from users.models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'author',)
    list_filter = ('pub_date', 'author', 'name', 'tags',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'username',)



admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(User, UserAdmin)
admin.site.register(Follow)
