from django.urls import path
from . import views

urlpatterns =[
    path('generate/', views.generateQR.as_view()),
    path('info/<str:key>/', views.scanQR),
    path('getQRs/',views.get_qrs.as_view()),
    path('history/',views.getScanHistory.as_view()),
    # path('chat/<str:room_name>/', views.chat_room, name='chat_room')
    # path('', views.index, name='index'),
]