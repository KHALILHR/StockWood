from django import forms
from .models import Stock,Container  # Update the import to use WoodStock instead of Stock

class StockForm(forms.ModelForm):
    container = forms.ModelChoiceField(
        queryset=Container.objects.all(),  # Queryset to get all containers
        empty_label="Select a Container",  # Optional: Add an empty label to the dropdown
        widget=forms.Select(attrs={'class': 'form-control'}),  # Add the 'form-control' class
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})
        self.fields['wood_type'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['length'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['width'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['thickness'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = Stock
        fields = ['name', 'container', 'quantity', 'wood_type', 'length', 'width', 'thickness', 'cubic_meter']

        
        
class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ['name', 'description']
        
