# Generated by Django 3.0.7 on 2023-11-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_auto_20231129_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerdetails',
            name='cgst',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='offerdetails',
            name='igst',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='offerdetails',
            name='total',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]