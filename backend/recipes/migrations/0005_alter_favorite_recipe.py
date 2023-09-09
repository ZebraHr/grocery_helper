# Generated by Django 4.2.4 on 2023-09-09 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_subscribe_delete_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_recipes', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
