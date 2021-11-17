from django.urls import path
from . import views


urlpatterns = [
    path('products/',views.ProductList.as_view()),
    path('products/<int:pk>',views.ProductDetail.as_view()),
    path('collection_list/',views.CollectionList.as_view()),
    path('collection_detail/<int:pk>',views.CollectionDetails.as_view()),
]