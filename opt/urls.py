from django.urls import path

from . import views

urlpatterns = [
    path('opt/', views.index, name='index'),
]
