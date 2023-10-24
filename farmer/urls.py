from django.urls import path
from .import views

app_name='farmer'

urlpatterns = [
    path('products/', views.products,name='products' ),
    path('add_products/', views.add_products, name='add_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),

]