from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin
from django.contrib.admin import display

from recipes.models import (Ingredient,
                            Tag,
                            Recipe,
                            Favorite,
                            ShoppingCart,
                            Subscribe,
                            IngredientAmount,
                            RecipeTag,
                            )
from users.models import User


@admin.register(Tag)
class RecipeIngredientAdmin(ImportExportActionModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class RecipeTagAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class TagInRecipeAdmin(admin.TabularInline):
    model = RecipeTag
    autocomplete_fields = ('tag', )


class IngredientAmountAdmin(admin.TabularInline):
    model = IngredientAmount
    autocomplete_fields = ('ingredient', )
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountAdmin, TagInRecipeAdmin)
    list_display = ('id', 'name', 'text', 'author', 'is_in_favorites')
    readonly_fields = ('is_in_favorites',)
    list_filter = ('pub_date', 'author', 'name', 'tags',)
    empty_value_display = '-пусто-'

    @display(description='Добавлено в избранное')
    def is_in_favorites(self, obj):
        return obj.favorites_recipes.count()


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'username',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(User, UserAdmin)
admin.site.register(Subscribe)
