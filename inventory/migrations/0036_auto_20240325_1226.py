# Generated by Django 3.0.7 on 2024-03-25 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_remove_stock_qt'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='length_a',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='width_a',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
