# Generated by Django 3.0.7 on 2023-11-14 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_auto_20231110_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Opened'), ('OUT_OF_STOCK', 'Out of Stock')], default='OPEN', max_length=15),
        ),
    ]
