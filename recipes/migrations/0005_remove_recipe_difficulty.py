# Generated by Django 4.2.5 on 2023-10-16 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_difficulty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='difficulty',
        ),
    ]
