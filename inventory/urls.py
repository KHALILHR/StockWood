from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
    path('add_container/', views.add_container, name='add_container'),
    path('containers/', views.container_list, name='container_list'),
    path('all_stock/', views.all_stock, name='all-stock'),

]