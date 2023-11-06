from django.db import models

class Container(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    wood_type = models.CharField(max_length=30)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    thickness = models.DecimalField(max_digits=5, decimal_places=2)
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
