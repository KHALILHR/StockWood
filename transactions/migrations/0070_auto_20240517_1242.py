# Generated by Django 3.0.7 on 2024-05-17 10:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0069_auto_20240512_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gstin', models.CharField(max_length=15, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='salebill',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='salebill',
            name='client',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='transactions.Client'),
            preserve_default=False,
        ),
    ]