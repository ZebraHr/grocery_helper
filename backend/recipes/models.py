from django.db import models
# from django.core.validators import MinValueValidator

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(max_length=150,
                            verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=150,
                                        verbose_name='Единица измерения')
    # добавить выпадающий список

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(max_length=150, verbose_name='Название тега')
    color = models.CharField(max_length=10, verbose_name='Цветовой код')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
        default=1,
        #   validators=(MinValueValidator(1, 'Минимум 1 минута')),
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
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        'Количество',
        #   validators=[MinValueValidator(1,
        #  message='Минимальное количество 1!')]
    )

    class Meta:
        ordering = ['recipe']

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTag(models.Model):
    """
    Вспомогательная модель.
    Для реализаци связи М2М между моделями Recipe
    и Tag.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        ordering = ['recipe']

    def __str__(self):
        return f'{self.recipe} {self.tag}'


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
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

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

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        models.UniqueConstraint(fields=['user', 'author'],
                                name='unique_ff')
