import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import normalize_newlines


# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance, **kwargs):
#     instance.image.delete(False)


class Chef(AbstractUser):
    favorite_recipes = models.ManyToManyField('Recipe')
    subscriptions = models.ManyToManyField(
        'self', symmetrical=False, through='Subscription'
    )

    class Meta(AbstractUser.Meta):
        ordering = ('first_name',)
        verbose_name = 'Кулинар'
        verbose_name_plural = 'Кулинары'

    def get_absolute_url(self):
        return reverse('chef', args=(self.pk,))


def get_sentinel_user():
    return Chef.objects.get_or_create(
        username='deleted', first_name='Удалённый пользователь'
    )[0]


class Tag(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = 'breakfast', 'Завтрак'
        LUNCH = 'lunch', 'Обед'
        DINNER = 'dinner', 'Ужин'

    colors = {
        'breakfast': 'orange',
        'lunch': 'green',
        'dinner': 'purple'
    }

    @property
    def color(self):
        return self.colors[self.name]

    name = models.CharField(
        max_length=9, choices=MealType.choices,
        unique=True, default=MealType.LUNCH
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class FoodProduct(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    unit = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    _original_author_name = models.CharField(
        max_length=150, editable=False, default='# not defined #'
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Chef, on_delete=models.SET(get_sentinel_user),
                               related_name='recipes')
    # image = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    ingredients = models.ManyToManyField(FoodProduct, through='Ingredient')
    tags = models.ManyToManyField(Tag)
    time_for_preparing = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        unique_together = ('_original_author_name', 'title')
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', args=(self.pk,))

    def description_as_list_of_paragraphs(self):
        value = normalize_newlines(self.description)
        paras = re.split('\n{2,}', str(value))
        return paras


@receiver(pre_save, sender=Recipe)
def init_original_author_name(sender, instance, *args, **kwargs):
    if instance._original_author_name != '# not defined #':
        return

    if hasattr(instance, 'author') and instance.author is not None:
        instance._original_author_name = instance.author.username


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food_product = models.ForeignKey(FoodProduct, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('recipe', 'food_product')
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Subscription(models.Model):
    subscriber = models.ForeignKey(Chef, on_delete=models.CASCADE,
                                   related_name='subscribers')
    author = models.ForeignKey(Chef, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'author')
        constraints = [
            models.CheckConstraint(
                name='cannot_follow_yourself',
                check=~models.Q(subscriber=models.F('author'))
            )
        ]
