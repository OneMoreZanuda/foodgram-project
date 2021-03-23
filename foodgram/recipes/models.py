from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField


User = get_user_model()


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


# @receiver(post_delete, sender=Post)
# def submission_delete(sender, instance, **kwargs):
#     instance.image.delete(False)


# class Tag(models.Model):
#     class MealType(models.TextChoices):
#         BREAKFAST = 'Завтрак'
#         LUNCH = 'Обед'
#         DINNER = 'Ужин'

#     name = models.CharField(
#         max_length=7, choices=MealType.choices, default=MealType.LUNCH
#     )

#     def __str__(self):
#         return self.name


TAGS = (('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'))


class FoodProduct(models.Model):
    name = models.CharField(max_length=200, primary_key=True, db_index=True)
    unit = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    _original_author_name = models.CharField(
        max_length=150, editable=False, default='# not defined #'
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user),
                               related_name='recipes')
    # image = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    ingredients = models.ManyToManyField(FoodProduct, through='Ingredient')
    # tags = models.ManyToManyField(Tag)
    tags = MultiSelectField(choices=TAGS, min_choices=1, default='lunch')
    time_for_preparing = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        unique_together = ('_original_author_name', 'title')
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food_product = models.ForeignKey(FoodProduct, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()


@receiver(pre_save, sender=Recipe)
def init_original_author_name(sender, instance, *args, **kwargs):
    if instance._original_author_name != '# not defined #':
        return

    if hasattr(instance, "author") and instance.author is not None:
        instance._original_author_name = instance.author.username
