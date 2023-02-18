from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import QR

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

import random,string

import io
from PIL import Image
import qrcode
import cloudinary, cloudinary.uploader, cloudinary.api
config=cloudinary.config(secure=True)

class generateQR(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user=request.user
        name = request.data.get('name')
        description = request.data.get('description')
        key = ''.join(random.choice(string.ascii_letters) for _ in range(50))
        while QR.objects.filter(key=key).exists():
            key = ''.join(random.choice(string.ascii_letters) for _ in range(50))
        qr=qrcode.make(('https://' if request.is_secure() else 'http://') + request.META['HTTP_HOST'] + '/info/' + key)
        stream = io.BytesIO()
        qr.save(stream, format="PNG")
        qr_bytes=qr_bytes = stream.getvalue()
        
        upload = cloudinary.uploader.upload(qr_bytes, public_id=key, unique_filename = True, overwrite=True, folder="TagIt")
        # print(upload)
        scURL = upload['secure_url']
        
        user_qr = QR.objects.create(user=user, name=name, description=description, key=key, qr=scURL)
        user_qr.save()
        return Response({'url':scURL,'status': 'success'})

# def index(request):
#     qr=qrcode.make('www.google.com')
#     stream = io.BytesIO()
#     qr.save(stream, format="PNG")
#     qr_bytes=qr_bytes = stream.getvalue()
#     cloudinary.uploader.upload(qr_bytes, public_id="hehe_qr", unique_filename = False, overwrite=True, folder="TagIt")

#     return render(request,"<h1>hello</h1>")