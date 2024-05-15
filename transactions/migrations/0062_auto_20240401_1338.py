# Generated by Django 3.0.7 on 2024-04-01 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0061_auto_20240306_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offeritem',
            name='per_price',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=30),
        ),
        migrations.AlterField(
            model_name='offeritem',
            name='total_price',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=30),
        ),
    ]