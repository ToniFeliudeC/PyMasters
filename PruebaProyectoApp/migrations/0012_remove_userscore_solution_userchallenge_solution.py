# Generated by Django 4.1.7 on 2023-05-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PruebaProyectoApp', '0011_userscore_solution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userscore',
            name='solution',
        ),
        migrations.AddField(
            model_name='userchallenge',
            name='solution',
            field=models.TextField(default=None),
        ),
    ]
