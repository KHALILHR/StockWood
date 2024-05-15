# Generated by Django 3.0.7 on 2024-03-05 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0058_auto_20240305_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='sale_type',
            field=models.CharField(choices=[('quantity', 'Quantity'), ('cubic_meter', 'Cubic Meter'), ('both', 'Both Quantity and Cubic Meter')], default='quantity', max_length=20),
        ),
        migrations.AlterField(
            model_name='offeritem',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True),
        ),
    ]