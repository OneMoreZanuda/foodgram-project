# Generated by Django 3.1.7 on 2021-03-14 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recipes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('food_product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.foodproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Завтрак', 'Breakfast'), ('Обед', 'Lunch'), ('Ужин', 'Dinner')], default='Обед', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measured_quantity', models.CharField(choices=[('Объём', 'Volume'), ('Масса', 'Mass'), ('Количество', 'Number')], default='Объём', max_length=150)),
                ('designation', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_real_author_name', models.CharField(editable=False, max_length=150)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('time_for_preparing', models.PositiveSmallIntegerField()),
                ('author', models.ForeignKey(on_delete=models.SET(recipes.models.get_sentinel_user), related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(through='recipes.Ingredient', to='recipes.FoodProduct')),
                ('tag', models.ManyToManyField(to='recipes.Tag')),
            ],
            options={
                'ordering': ('title',),
                'unique_together': {('_real_author_name', 'title')},
            },
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='units',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.unit'),
        ),
    ]
