from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('complex_query/',views.complex_query),
    path('sorting/',views.sorting),
    path('inner/',views.inner_join),
    path('select_related',views.select_related),
]
