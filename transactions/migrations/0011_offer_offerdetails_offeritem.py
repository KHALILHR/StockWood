# Generated by Django 3.0.7 on 2023-11-28 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_remove_stock_qt'),
        ('transactions', '0010_auto_20231121_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('offer_no', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('gstin', models.CharField(max_length=15)),
                ('sale_type', models.CharField(choices=[('quantity', 'Quantity'), ('cubic_meter', 'Cubic Meter')], default='quantity', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OfferItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cubic_meter', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('per_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('quantity', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('offer_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_items', to='transactions.Offer')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_items', to='inventory.Stock')),
            ],
        ),
        migrations.CreateModel(
            name='OfferDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eway', models.CharField(blank=True, max_length=50, null=True)),
                ('veh', models.CharField(blank=True, max_length=50, null=True)),
                ('destination', models.CharField(blank=True, max_length=50, null=True)),
                ('po', models.CharField(blank=True, max_length=50, null=True)),
                ('cgst', models.CharField(blank=True, max_length=50, null=True)),
                ('sgst', models.CharField(blank=True, max_length=50, null=True)),
                ('igst', models.CharField(blank=True, max_length=50, null=True)),
                ('cess', models.CharField(blank=True, max_length=50, null=True)),
                ('tcs', models.CharField(blank=True, max_length=50, null=True)),
                ('total', models.CharField(blank=True, max_length=50, null=True)),
                ('offer_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_details', to='transactions.Offer')),
            ],
        ),
    ]
