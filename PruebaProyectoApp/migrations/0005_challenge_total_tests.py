# Generated by Django 4.1.7 on 2023-05-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PruebaProyectoApp', '0004_alter_challenge_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='total_tests',
            field=models.IntegerField(default=0),
        ),
    ]
