# Generated by Django 3.0.7 on 2024-02-21 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0047_auto_20231223_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salebill',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]