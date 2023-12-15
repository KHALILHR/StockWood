# Generated by Django 3.0.7 on 2023-11-14 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0026_auto_20231114_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Opened'), ('STOCKED', 'Stocked'), ('OUT_OF_STOCK', 'Out of Stock')], default='OPEN', max_length=15),
        ),
    ]