# Generated by Django 3.0.7 on 2023-12-05 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0026_auto_20231205_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebill',
            name='facture_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]