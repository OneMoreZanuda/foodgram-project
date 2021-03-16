from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, post_init
from django.dispatch import receiver


User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance, **kwargs):
#     instance.image.delete(False)


class FoodProduct(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = 'Завтрак'
        LUNCH = 'Обед'
        DINNER = 'Ужин'

    name = models.CharField(
        max_length=7, choices=MealType.choices, default=MealType.LUNCH
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    _real_author_name = models.CharField(max_length=150, editable=False)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user),
                               related_name='recipes')
    # image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    ingredients = models.ManyToManyField(FoodProduct, through='Ingredient')
    tags = models.ManyToManyField(Tag)
    time_for_preparing = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('_real_author_name', 'title')
        ordering = ('title',)

    def __str__(self):
        return self.title


@receiver(post_init, sender=Recipe)
def init_real_author_name(sender, instance, **kwargs):
    instance._real_author_name = instance.author.username if hasattr(instance, "author") else 'not defined'


class Unit(models.Model):
    class Quantity(models.TextChoices):
        VOLUME = 'Объём'
        MASS = 'Масса'
        NUMBER = 'Количество'

    measured_quantity = models.CharField(
        max_length=150,
        choices=Quantity.choices,
        default=Quantity.VOLUME
    )
    designation = models.CharField(max_length=150)

    def __str__(self):
        return self.designation


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food_product = models.ForeignKey(FoodProduct, on_delete=models.PROTECT)
    quantity = models.FloatField()
    units = models.ForeignKey(Unit, on_delete=models.PROTECT)
