# Generated by Django 3.1.1 on 2020-12-30 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201229_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.PositiveIntegerField(default=0),
        ),
    ]