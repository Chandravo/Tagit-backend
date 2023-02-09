from django.urls import path
from . import views

urlpatterns =[
    path('login/', views.login.as_view()),
    path('register/', views.register.as_view()),
    path('',views.check),
    # path('', views.index, name='index'),
]