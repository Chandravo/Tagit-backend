from django.urls import path
from . import views

urlpatterns =[
    path('generate/', views.generateQR.as_view()),
    path('info/<str:key>/', views.scanQR),
    # path('', views.index, name='index'),
]