# Generated by Django 4.1.7 on 2023-05-15 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PruebaProyectoApp', '0014_alter_userchallenge_unique_together_delete_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='category',
            field=models.TextField(default=''),
        ),
    ]
