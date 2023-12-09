import math
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    OfferDetails,
    PurchaseBill, 
    Supplier, 
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,  
    SaleItem,
    SaleBillDetails
)
from .forms import (
    SelectSupplierForm, 
    PurchaseItemFormset,
    PurchaseDetailsForm, 
    SupplierForm, 
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm
)
from inventory.models import Stock




# shows a lists of all suppliers
class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier
class SupplierCreateView(SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier has been created successfully"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context     


# used to update a supplier's info
class SupplierUpdateView(SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier details has been updated successfully"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()                                               
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile
class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier'  : supplierobj,
            'bills'     : bills
        }
        return render(request, 'suppliers/supplier.html', context)




# shows the list of bills of all purchases 
class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to select the supplier
class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})


# used to generate a bill object and save items
class PurchaseCreateView(View):                                                 
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)                      # renders an empty formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)                             # recieves a post method for the formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = PurchaseBill(supplier=supplierobj)                        # a new object of class 'PurchaseBill' is created with supplier field set to 'supplierobj'
            billobj.save()                                                      # saves object into the db
            # create bill details object
            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)       # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity                              # updates quantity
                # saves bill item and stock
                stock.save()
                billitem.save()
            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Purchase bill has been deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)




# shows the list of bills of all sales 
class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to generate a bill object and save items
from django.shortcuts import redirect

from django.shortcuts import redirect

class SaleCreateView(View):
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)
        context = {
            'form': form,
            'formset': formset,
            'stocks': Stock.objects.filter(is_deleted=False)
        }

        stock_error = False  # Flag to check for stock errors

        if form.is_valid() and formset.is_valid():
            billobj = form.save(commit=False)
       
            billobj.save()
            stock_error = False
            billobj.save()
           
            for form_item in formset:
                billitem = form_item.save(commit=False) 
                stock = get_object_or_404(Stock, name=billitem.stock.name)

                if billobj.sale_type == 'cubic_meter':
                    billitem.totalprice = billitem.perprice * billitem.cubic_meter
                    if billitem.cubic_meter > stock.cubic_meter:
                        stock_error = True
                        break
                    stock.cubic_meter -= billitem.cubic_meter
                else:  # 'quantity' sale type
                    billitem.totalprice = billitem.perprice * billitem.quantity
                    if billitem.quantity > stock.quantity:
                        stock_error = True
                        break
                    stock.quantity -= billitem.quantity

                billitem.billno = billobj  # Assign the Sale object to the SaleItem's billno field
                billitem.save()
                stock.save()

            if stock_error:
                stock_name = stock.name  # Assuming stock.name is the name field in the Stock model
                error_message = f"{'' if billobj.sale_type == 'cubic_meter' else 'Quantity'} exceeds available stock for {stock_name}."
                messages.error(request, error_message)
                return render(request, self.template_name, context)
            else:
                 billobj.save()  # Save the Sale object along with SaleBillDetails
                 billdetailsobj = SaleBillDetails(billno=billobj)
                 billdetailsobj.save()
                 messages.success(request, "Sold items have been registered successfully")
                 return redirect('sale-bill', billno=billobj.billno)

        return render(request, self.template_name, context)




# used to delete a bill object
class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            
        messages.success(self.request, "Sale bill has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)




# used to display the purchase bill object
class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)


# used to display the sale bill object
class SaleBillView(View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)




class FactureView(View):
    model = SaleBill  # Assuming that FactureView uses SaleBill model; you can replace it with the appropriate model if needed
    template_name = 'bill/facture.html'
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : self.model.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")
            
            
            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : self.model.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)



from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import OfferForm, OfferItemFormset
from .models import Offer, OfferItem, Stock
from django.contrib import messages
from .models import Offer

# views.py
from django.shortcuts import render
from django.views import View
from .forms import OfferSearchForm

class OfferListView(View):
    template_name = 'sales/offer_list.html'

    def get(self, request):
        form = OfferSearchForm(request.GET)
        
        if form.is_valid():
            customer_name = form.cleaned_data.get('customer_name')
            
            # Filter the queryset based on the customer name
            if customer_name:
                offers = Offer.objects.filter(name__icontains=customer_name)
            else:
                # If no customer name is provided, show all offers
                offers = Offer.objects.all()
        else:
            # If form is not valid, show all offers
            offers = Offer.objects.all()

        context = {'offers': offers, 'form': form}
        return render(request, self.template_name, context)
     
    
from django.shortcuts import render, redirect
from django.views import View
from .forms import OfferForm, OfferItemFormset
from .models import Stock, OfferDetails
from django.contrib import messages
import math

class OfferCreateView(View):
    template_name = 'sales/new_offre.html'

    def get(self, request):
        form = OfferForm(request.GET or None)
        formset = OfferItemFormset(request.GET or None)
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = OfferForm(request.POST)
        formset = OfferItemFormset(request.POST)
        context = {
            'form': form,
            'formset': formset,
            'stocks': Stock.objects.filter(is_deleted=False)
        }

        if form.is_valid() and formset.is_valid():
            billobj = form.save()  # Save the Offer object first

            billdetailsobj = OfferDetails(offer_no=billobj)
            billdetailsobj.save()

            for form_item in formset:
                billitem = form_item.save(commit=False)
                billitem.offer_no = billobj  # Assign the Offer object to the OfferItem's offer_no field

                # Update the total_price field with the calculated total price
                cubic_meter = form_item.cleaned_data.get('cubic_meter')
                quantity = form_item.cleaned_data.get('quantity')
                per_price = form_item.cleaned_data.get('per_price')
            
                if billobj.sale_type == 'quantity' and not math.isnan(quantity):
                    billitem.total_price = quantity * per_price
                elif not math.isnan(cubic_meter):
                    billitem.total_price = cubic_meter * per_price

                billitem.save()

            messages.success(request, "Offer items have been registered successfully")
            return redirect('offer-bill', offer_no=billobj.offer_no)

        # If the form or formset is not valid, return the response
        return render(request, self.template_name, context)


from django.shortcuts import render, redirect
from django.views import View
from .models import Offer, OfferItem, OfferDetails
from .forms import OfferDetailsForm
class OfferBillView(View):
    model = Offer
    template_name = "bill/offre_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, offer_no):
        context = {
            'offer'         : Offer.objects.get(offer_no=offer_no),
            'items'         : OfferItem.objects.filter(offer_no=offer_no),
            'offerdetails'   : OfferDetails.objects.get(offer_no=offer_no),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, offer_no):
        form = OfferDetailsForm(request.POST)
        if form.is_valid():
            offer_details_obj = OfferDetails.objects.get(offer_no=offer_no)
            
            offer_details_obj.eway = request.POST.get("eway")    
            offer_details_obj.veh = request.POST.get("veh")
            offer_details_obj.destination = request.POST.get("destination")
            offer_details_obj.po = request.POST.get("po")
            offer_details_obj.cgst = request.POST.get("cgst")
            offer_details_obj.sgst = request.POST.get("sgst")
            offer_details_obj.igst = request.POST.get("igst")
            offer_details_obj.cess = request.POST.get("cess")
            offer_details_obj.tcs = request.POST.get("tcs")
            offer_details_obj.total = request.POST.get("total")

            offer_details_obj.save()
            
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'offer'         : Offer.objects.get(offer_no=offer_no),
            'items'         : OfferItem.objects.filter(offer_no=offer_no),
            'offerdetails'   : OfferDetails.objects.get(offer_no=offer_no),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

from django.shortcuts import get_object_or_404

def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)

    # Delete associated OfferItems
    offer_items = offer.offer_items.all()
    for offer_item in offer_items:
        offer_item.delete()

    # Now, delete the Offer
    offer.delete()

    return redirect('offer-list')
