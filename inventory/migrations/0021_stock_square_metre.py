# Generated by Django 3.0.7 on 2023-11-09 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_remove_stock_square_meters'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='square_metre',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]