# Generated by Django 3.0.7 on 2023-12-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0032_remove_salebill_facture_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='salebill',
            name='numero_facture',
            field=models.IntegerField(default=0),
        ),
    ]
