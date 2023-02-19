from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User

import io
from PIL import Image
import qrcode
import cloudinary, cloudinary.uploader, cloudinary.api
config=cloudinary.config(secure=True)

class register(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        phone = request.data.get('phone')
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(email,phone,password)
        user.save()
        
        return Response({'status':'success'},status=status.HTTP_201_CREATED)
class login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
       
        print(email,password)
        print()
        
        user = authenticate(request, email=email, password=password)

        if user is None:
            print("lol")
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        token = Token.objects.get_or_create(user=user)

        data = {
            'key': token[0].key,
            'email': user.email,
        }

        return Response(data, status=status.HTTP_200_OK)


def check(request):
    return render (request,'1.html')