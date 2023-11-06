from django.shortcuts import render
from django.views.generic import View, TemplateView
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        labels = []
        data = []
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        alerts = []

        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)

            # Set your threshold value (e.g., 10)
            threshold = 10

            if item.quantity < threshold:
                alert_message = f"Low stock: {item.name} (Quantity: {item.quantity})"
                alerts.append(alert_message)

        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels': labels,
            'data': data,
            'sales': sales,
            'purchases': purchases,
            'alerts': alerts,  # Include the alerts in the context
        }
        return render(request, self.template_name, context)


class AboutView(TemplateView):
    template_name = "about.html"

    