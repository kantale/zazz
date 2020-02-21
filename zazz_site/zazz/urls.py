from django.urls import path

from . import views

urlpatterns = [
        path('', views.index),
        path('sample_table/', views.sample_table),
        path('Barcode_Name/', views.Barcode_Name),
        path('get_database_checkbox/', views.get_database_checkbox),
        path('get_database_slider/', views.get_database_slider),
        path('update_table/', views.update_table),
]



