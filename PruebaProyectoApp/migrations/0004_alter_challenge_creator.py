# Generated by Django 4.1.7 on 2023-05-03 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PruebaProyectoApp', '0003_delete_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
