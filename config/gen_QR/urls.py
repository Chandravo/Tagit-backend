from django.urls import path
from . import views

urlpatterns =[
    path('generate/', views.generate.as_view()),
    # path('', views.index, name='index'),
]