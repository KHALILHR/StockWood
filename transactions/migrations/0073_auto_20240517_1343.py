# Generated by Django 3.0.7 on 2024-05-17 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0072_salebill_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salebill',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='client',
            name='payment_method',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
