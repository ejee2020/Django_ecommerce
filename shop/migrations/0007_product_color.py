# Generated by Django 3.1.1 on 2020-12-30 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_product_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('Black', 'Black'), ('Blue', 'Blue'), ('Brown', 'Brown'), ('Burgundy', 'Burgundy'), ('Camel', 'Camel'), ('Green', 'Green'), ('Grey', 'Grey'), ('Navy', 'Navy'), ('Orange', 'Orange'), ('Pink', 'Pink'), ('Purple', 'Purple'), ('Red', 'Red'), ('White', 'White'), ('Yellow', 'Yellow')], default='', max_length=20),
        ),
    ]
