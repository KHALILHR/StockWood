# Generated by Django 3.0.7 on 2023-11-01 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_remove_stock_container_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
