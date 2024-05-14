from django import forms
from django.forms import formset_factory
from .models import (
    Offer,
    OfferDetails,
    OfferItem,
    Supplier, 
    PurchaseBill, 
    PurchaseItem,
    PurchaseBillDetails, 
    SaleBill, 
    SaleItem,
    SaleBillDetails
)
from inventory.models import Stock


# form used to select a supplier
class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_deleted=False)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseBill
        fields = ['supplier']

# form used to render a single stock item form
class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(is_deleted=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = PurchaseItem
        fields = ['stock', 'quantity', 'perprice']

# formset used to render multiple 'PurchaseItemForm'
PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)

# form used to accept the other details for purchase bill
class PurchaseDetailsForm(forms.ModelForm):
    class Meta:
        model = PurchaseBillDetails
        fields = ['eway','veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']


# form used for supplier
class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Alphabets and Spaces only'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '8', 'pattern' : '[0-9]{8}', 'title' : 'Numbers only'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern' : '[A-Z0-9]{15}', 'title' : 'GSTIN Format Required'})
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'email', 'gstin']
        widgets = {
            'address' : forms.Textarea(
                attrs = {
                    'class' : 'textinput form-control',
                    'rows'  : '4'
                }
            )
        }


# form used to get customer details
from django import forms
from .models import SaleBill


class SaleForm(forms.ModelForm):
    SALE_TYPE_CHOICES = [
        ('quantity', 'Sale per Quantity'),
        ('cubic_meter', 'Sale per Cubic Meter'),
        ('both', 'Both Quantity and Cubic Meter'),
    ]

    EXTRA_OPTIONS_CHOICES = [
        ('facture_bon_livraison', 'Facture and Bon de Livraison'),
        ('bon_de_livraison', 'Bon de Livraison'),
    ]

    sale_type = forms.ChoiceField(
        choices=SALE_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='quantity',
    )

    extra_options = forms.ChoiceField(
        choices=EXTRA_OPTIONS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='bon_de_livraison',
    )
    time = forms.DateTimeField(
        label='Time',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    class Meta:
        model = SaleBill
        fields = ['name', 'phone', 'address', 'email', 'gstin', 'sale_type', 'extra_options','time', 'numero_facture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_facture': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# form used to render a single stock item form
class SaleItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['cubic_meter'].widget.attrs.update({'class': 'textinput form-control setprice cubic_meter', 'required': 'true'})

        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'type': 'number', 'step': '1', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})

        # Dynamically update choices for the 'stock' field
        self.fields['stock'].choices = self.get_stock_choices()

    def get_stock_choices(self):
        """
        Method to generate choices for the 'stock' field.
        Each choice consists of the stock name, its cubic meter, and its primary key.
        """
        queryset = Stock.objects.filter(is_deleted=False)
        choices = [(stock.pk, f"{stock.name} ({stock.cubic_meter}m³, {stock.quantity} Piece)")
           for stock in queryset if stock.cubic_meter != 0]
        return choices



    class Meta:
        model = SaleItem
        fields = ['stock','cubic_meter', 'quantity', 'perprice']
        widgets = {
            'stock': forms.Select(attrs={'class': 'textinput form-control setprice stock', 'required': 'true'}),
            # ... other fields
        }
        field_classes = {
            'perprice': forms.DecimalField,
        }
        

# formset used to render multiple 'SaleItemForm'
SaleItemFormset = formset_factory(SaleItemForm, extra=1)

# form used to accept the other details for sales bill
class SaleDetailsForm(forms.ModelForm):
    class Meta:
        model = SaleBillDetails
        fields = ['eway','veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']


from django import forms



from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    SALE_TYPE_CHOICES = [
        ('quantity', 'Sale per Quantity'),
        ('cubic_meter', 'Sale per Cubic Meter'),
        ('both', 'Both Quantity and Cubic Meter'),
    ]

    sale_type = forms.ChoiceField(
        choices=SALE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='quantity',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['email'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['gstin'].widget.attrs.update({'class': 'textinput form-control'})
        # Add other field customizations as needed

    class Meta:
        model = Offer
        fields = ['name', 'phone', 'address', 'email', 'gstin', 'sale_type']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'textinput form-control', 'rows': '4'}),
        }


class OfferItemForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['cubic_meter'].widget.attrs.update({'class': 'textinput form-control setprice cubic_meter', 'required': 'true'})

        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'type': 'number', 'step': '1', 'min': '0', 'required': 'true'})
        self.fields['per_price'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})

        # Dynamically update choices for the 'stock' field
        self.fields['stock'].choices = self.get_stock_choices()

    def get_stock_choices(self):
        """
        Method to generate choices for the 'stock' field.
        Each choice consists of the stock name and its cubic meter.
        """
        queryset = Stock.objects.filter(is_deleted=False)
        choices = [(stock.pk, f"{stock.name} ({stock.cubic_meter}m³, {stock.quantity} Piece)")
           for stock in queryset if stock.cubic_meter != 0]
        return choices


    class Meta:
        model = OfferItem
        fields = ['stock','cubic_meter', 'quantity', 'per_price']
        widgets = {
            'stock': forms.Select(attrs={'class': 'textinput form-control setprice stock', 'required': 'true'}),
        }
        field_classes = {
            'per_price': forms.DecimalField,
        }

OfferItemFormset = forms.formset_factory(OfferItemForm, extra=1)



class OfferDetailsForm(forms.ModelForm):
    class Meta:
        model = OfferDetails
        fields = ['eway', 'veh', 'destination', 'po', 'cgst', 'sgst', 'igst', 'cess', 'tcs', 'total']
        # Customize widget attributes as needed for OfferDetails form
        


class ContainerSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False, label='Search by container name')

# forms.py
from django import forms

class OfferSearchForm(forms.Form):
    customer_name = forms.CharField(required=False, label='Customer Name')
