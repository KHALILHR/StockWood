# Generated by Django 3.0.7 on 2024-05-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0073_auto_20240517_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_offer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='is_salebill',
            field=models.BooleanField(default=False),
        ),
    ]
