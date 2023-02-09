from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

class generate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user=request.user
            