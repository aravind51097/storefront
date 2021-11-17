from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

router=DefaultRouter()
router.register('product',views.ProductViewSet)
router.register('collection',views.CollectionViewSet)


urlpatterns = router.urls