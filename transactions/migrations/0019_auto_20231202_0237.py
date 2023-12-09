# Generated by Django 3.0.7 on 2023-12-02 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_auto_20231129_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='sale_type',
            field=models.CharField(choices=[('quantity', 'Quantity'), ('cubic_meter', 'Cubic Meter')], default='cubic_meter', max_length=20),
        ),
    ]
