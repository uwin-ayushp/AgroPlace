from django.urls import path
from .import views

app_name='farmer'

urlpatterns = [
    path('products/', views.products,name='products' ),
    path('add_products/', views.add_products, name='add_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('orders/<int:user_id>/', views.farmerOrder, name='farmerOrder'),
    path('change-status/<int:order_id>/', views.change_status, name='change_status'),

    path('insights/', views.insights, name='insights'),
    path('expert_advice/',views.expert_advice,name='expert_advice'),
    path('inbox/',views.expert_advice,name='Inbox')
]