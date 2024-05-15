# Generated by Django 3.0.7 on 2024-02-23 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0051_auto_20240223_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleitem',
            name='sale_type',
        ),
        migrations.AddField(
            model_name='salebill',
            name='sale_type',
            field=models.CharField(choices=[('quantity', 'Sale per Quantity'), ('cubic_meter', 'Sale per Cubic Meter')], default='quantity', max_length=20),
        ),
    ]