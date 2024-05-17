from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView,
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from transactions.forms import ContainerSearchForm
from .models import Stock
from .forms import ContainerForm, StockForm
from django_filters.views import FilterView
from .filters import StockFilter

class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Group stocks by container name
        grouped_stocks = {}
        for stock in context['object_list']:
            container_name = stock.container.name if stock.container else 'No Container'
            if container_name not in grouped_stocks:
                grouped_stocks[container_name] = []
            grouped_stocks[container_name].append(stock)

        # Convert the grouped data to a list for the template
        context['grouped_stocks'] = [{'container_name': container_name, 'stocks': stocks} for container_name, stocks in grouped_stocks.items()]

        return context



class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "edit_stock.html"
    success_url = '/inventory'
    success_message = "Stock has been created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context

class StockUpdateView(SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "edit_stock.html"
    success_url = '/inventory'
    success_message = "Stock has been updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'
        return context

class StockDeleteView(View):
    template_name = "delete_stock.html"
    success_message = "Stock has been deleted successfully"
    def get_queryset(self):
        # Filter out stocks that are marked as deleted
        return Stock.objects.filter(is_deleted=False)

    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object': stock})

    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        stock.is_deleted = True
        stock.save()
        messages.success(request, self.success_message)
        return redirect('all-stock')
    
def add_container(request):
    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('container_list')  # Redirect to a page showing the list of containers
    else:
        form = ContainerForm()
    
    return render(request, 'add_container.html', {'form': form})
from django.shortcuts import render
from .models import Container

def container_list(request):
    containers = Container.objects.all()
    search_form = ContainerSearchForm(request.GET)
    
    if search_form.is_valid():
        name = search_form.cleaned_data.get('name')
        if name:
            containers = containers.filter(name__icontains=name)
    
    context = {
        'containers': containers,
        'search_form': search_form,
    }
    return render(request, 'container_list.html', context)
from django.shortcuts import render
from .models import Stock  # Assuming your Stock model is imported from the models file

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Stock

from django.db.models import Sum

def all_stock(request):
    # Exclude stocks that are marked as deleted
    stock_list = Stock.objects.filter(is_deleted=False)

    # Calculate total quantity and total cubic meters
    total_quantity = stock_list.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_cubic_meters = stock_list.aggregate(Sum('cubic_meter'))['cubic_meter__sum'] or 0

    # Pass the full list of stocks to the template without pagination
    stocks = stock_list

    return render(request, 'all_stock.html', {'stocks': stocks, 'total_quantity': total_quantity, 'total_cubic_meters': total_cubic_meters})
