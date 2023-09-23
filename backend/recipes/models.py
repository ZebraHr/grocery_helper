from django.db import models
from django.core import validators

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(max_length=150,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=150,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        db_table = 'recipes_ingredient'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(max_length=150, unique=True,
                            verbose_name='Название тега')
    color = models.CharField(max_length=10, unique=True,
                             verbose_name='Цветовой код')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        db_table = 'recipes_tag'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField(verbose_name='Текст рецепта',
                            help_text='Введите текст рецепта',
                            )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Название ингредиента',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[validators.MinValueValidator(1)]
        )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Вспомогательная модель.
    Для реализаци связи М2М между моделями Recipe
    и Ingredient.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_in_ingr')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingr_in_recipes')
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[validators.MinValueValidator(1)]
    )

    class Meta:
        ordering = ['recipe']

    def __str__(self):
        return f'В {self.recipe} есть {self.ingredient}'


class RecipeTag(models.Model):
    """
    Вспомогательная модель.
    Для реализаци связи М2М между моделями Recipe
    и Tag.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_in_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='tag_in_recipes')

    class Meta:
        ordering = ['recipe']

    def __str__(self):
        return f'Рецепт {self.recipe} отмечен тегом {self.tag}'


class Favorite(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites_recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        models.UniqueConstraint(fields=['user', 'recipe'],
                                name='unique_u_f')

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    """Модель корзины покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        models.UniqueConstraint(fields=['user', 'recipe'],
                                name='unique_s_l')

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'


class Subscribe(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['author']
        models.UniqueConstraint(fields=['user', 'author'],
                                name='unique_ua')


class IngredientAmount(models.Model):
    """Модель вывода количества ингредиенто в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[validators.MinValueValidator(1)]
    )
