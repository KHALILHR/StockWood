# Generated by Django 3.0.7 on 2023-11-01 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20231101_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='container_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
