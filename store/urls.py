from django.urls import path
from . import views


urlpatterns = [
    path('products/',views.ProductList.as_view()),
    path('products/<int:id>',views.product_details),
    path('collection_list/',views.collection_list),
    path('collection_detail/<int:pk>',views.collection_detail),
]