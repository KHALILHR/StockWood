from django.db import models, transaction
from django.db import models
from inventory.models import Stock
from django.utils import timezone

# contains suppliers


class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    gstin = models.CharField(max_length=15, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name='purchasesupplier')


def __str__(self):
    return "Bill no: " + str(self.billno)


def get_items_list(self):
    return PurchaseItem.objects.filter(billno=self)


def get_total_price(self):
    purchaseitems = PurchaseItem.objects.filter(billno=self)
    total = 0
    for item in purchaseitems:
        total += item.totalprice
    return total

# contains the purchase stocks made


class PurchaseItem(models.Model):
    billno = models.ForeignKey(
        PurchaseBill, on_delete=models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

# contains the other details in the purchases bill


class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(
        PurchaseBill, on_delete=models.CASCADE, related_name='purchasedetailsbillno')

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)

    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno)


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=False)
    gstin = models.CharField(max_length=15, unique=True)
    payment_method = models.CharField(max_length=150)
    is_offer = models.BooleanField(default=False)
    is_salebill = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LastFactureNumber(models.Model):
    last_facture_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.last_facture_number)

class SaleBill(models.Model):
    SALE_TYPE_CHOICES = [
        ('quantity', 'Sale per Quantity'),
        ('cubic_meter', 'Sale per Cubic Meter'),
        ('both', 'Both Quantity and Cubic Meter'),
    ]

    EXTRA_OPTIONS_CHOICES = [
        ('facture_bon_livraison', 'Facture and Bon de Livraison'),
        ('bon_de_livraison', 'Bon de Livraison'),
    ]

    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)
    numero_facture = models.IntegerField(default=0)

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    gstin = models.CharField(max_length=30, blank=True)
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='quantity')
    client = models.OneToOneField(Client, on_delete=models.CASCADE ,null=True)
    extra_options = models.CharField(max_length=25, choices=EXTRA_OPTIONS_CHOICES, default='bon_de_livraison')
    

    def save(self, *args, **kwargs):
        if not self.sale_type and not self.extra_options:
            raise ValueError("At least one option must be selected.")

        if not self.pk:
            if self.extra_options == 'facture_bon_livraison':
                last_facture_number_obj, created = LastFactureNumber.objects.get_or_create()
                self.numero_facture = last_facture_number_obj.last_facture_number + 1
                last_facture_number_obj.last_facture_number = self.numero_facture
                last_facture_number_obj.save()

        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        # Before deleting the sale bill, decrement the facture number
        if self.extra_options == 'facture_bon_livraison':
            last_facture_number_obj = LastFactureNumber.objects.first()
            if last_facture_number_obj:
                last_facture_number_obj.last_facture_number -= 1
                last_facture_number_obj.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return "Bill no: " + str(self.billno)

    def __str__(self):
        return "Bill no: " + str(self.billno)


def get_items_list(self):
    return SaleItem.objects.filter(billno=self)


def get_total_price(self):
    saleitems = SaleItem.objects.filter(billno=self)
    total = 0
    for item in saleitems:
        total += item.totalprice
    return total

# contains the sale stocks made


class SaleItem(models.Model):
    billno = models.ForeignKey(
        SaleBill, on_delete=models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='saleitem')
    cubic_meter = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    perprice = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    totalprice = models.DecimalField(
        max_digits=30, decimal_places=3, default=0)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name


# contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(
        SaleBill, on_delete=models.CASCADE, related_name='saledetailsbillno')

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)

    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno)


class Offer(models.Model):
    SALE_TYPE_CHOICES = [
        ('quantity', 'Quantity'),
        ('cubic_meter', 'Cubic Meter'),
        ('both', 'Both Quantity and Cubic Meter'),

    ]
    offer_no = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    gstin = models.CharField(max_length=30, blank=True)
    sale_type = models.CharField(
        max_length=20, choices=SALE_TYPE_CHOICES, default='quantity')

    def __str__(self):
        return "Offer no: " + str(self.offer_no)

    def get_items_list(self):
        return OfferItem.objects.filter(offer_no=self)

    def get_total_price(self):
        offer_items = OfferItem.objects.filter(offer_no=self)
        total = 0
        for item in offer_items:
            total += item.total_price
        return total


class OfferItem(models.Model):
    offer_no = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='offer_items')
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name='offer_items')
    cubic_meter = models.DecimalField(
        max_digits=30, decimal_places=3, blank=True, null=True)
    per_price = models.DecimalField(max_digits=30, decimal_places=3, default=0)
    total_price = models.DecimalField(
        max_digits=30, decimal_places=3, default=0)

    quantity = models.DecimalField(
        max_digits=10, decimal_places=3, null=True, blank=True, default=0)

    def __str__(self):
        return "Offer no: " + str(self.offer_no.offer_no) + ", Item = " + self.stock.name


class OfferDetails(models.Model):
    offer_no = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='offer_details')

    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)

    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "Offer no: " + str(self.offer_no.offer_no)
