from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Ингридиент'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    ORANGE = '#FFA500'
    GREEN = '#008000'
    YELLOW = '#FFFF00'
    BLUE = '#0000FF'

    COLOR_CHOICES = [
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (YELLOW, 'Желтый'),
        (BLUE, 'Синий'),
    ]
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тэга'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        choices=COLOR_CHOICES,
        default=BLUE,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientInRecipe',
        verbose_name='Ингридиенты в рецепте'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата'
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True,
        verbose_name='Картинка'
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Минимальное время 1 минута!'),
        ],
        verbose_name='Время приготовления (в минутах)',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Минимальное значение 1!'),
        ],
        verbose_name='Количество ингридиента',
    )

    class Meta:
        verbose_name = 'Ингридиенты рецепта'
        verbose_name_plural = 'Ингридиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_name_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_name_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingСart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart_recipe',
    )

    class Meta:
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoppingcart'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'
