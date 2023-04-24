from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('product-detail/<str:pk>', views.about_product),
    path('current-category/<str:pk>', views.category_products),
    path('search-product', views.search_for_product),
    path('add-product/<int:pk>', views.add_product_to_cart),
    path('cart', views.get_user_cart),
    path('delete-product/<int:pk>', views.delete_pr_from_cart),
    path('order', views.order_zakaz)
]
