from django.db import models

class Container(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
from django.db import models

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    wood_type = models.CharField(max_length=30)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    cubic_meter = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, blank=True, null=True)
    STATUS_CHOICES = (
        ('OPEN', 'Opened'),
        ('STOCKED', 'Stocked'),
        ('OUT_OF_STOCK', 'Out of Stock'),
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OPEN')

    def save(self, *args, **kwargs):
        current_cubic_meter = self.__class__.objects.filter(pk=self.pk).values_list('cubic_meter', flat=True).first()

        if self.cubic_meter == 0:
            self.status = 'OUT_OF_STOCK'
        elif self.cubic_meter is not None:
            if current_cubic_meter is None or self.cubic_meter > current_cubic_meter:
                self.status = 'STOCKED'
            else:
                self.status = 'OPEN'

        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


