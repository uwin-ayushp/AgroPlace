from django.urls import path
from .import views

app_name='store'

urlpatterns = [
    path('home/',views.store, name='home'),
    path('recommendations/', views.get_recommendations, name='recommendations'),
    path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('submit_review/<int:product_id>/',views.submit_reviews,name='submit_reviews'),
    path('home/', views.sortProducts, name='sort_home'),
    path('home/', views.catProducts, name='catsort_home')
]
