# Generated by Django 3.0.7 on 2023-11-01 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20231101_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]