# Generated by Django 3.1.1 on 2020-12-29 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20201229_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='size_and_fit',
            new_name='size_and_fits',
        ),
    ]
