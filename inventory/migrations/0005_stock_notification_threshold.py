# Generated by Django 3.0.7 on 2023-10-30 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_remove_stock_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='notification_threshold',
            field=models.IntegerField(default=10),
        ),
    ]