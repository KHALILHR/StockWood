# Generated by Django 3.0.7 on 2024-05-17 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0071_auto_20240517_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebill',
            name='payment_method',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
