from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import QR
from .serializers import QRSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import random,string
from registration.models import User

import io
from PIL import Image
import qrcode
import cloudinary, cloudinary.uploader, cloudinary.api
config=cloudinary.config(secure=True)

class generateQR(APIView):
    # permission_classes = [IsAuthenticated,]

    def post(self, request):
        user=User.objects.all().first()
        name = request.data.get('name')
        description = request.data.get('description')
        key = ''.join(random.choice(string.ascii_letters) for _ in range(50))
        while QR.objects.filter(key=key).exists():
            key = ''.join(random.choice(string.ascii_letters) for _ in range(50))
        target = ('https://' if request.is_secure() else 'http://') + request.META['HTTP_HOST'] + '/info/' + key
        qr=qrcode.make(target)
        stream = io.BytesIO()
        qr.save(stream, format="PNG")
        qr_bytes=qr_bytes = stream.getvalue()
        
        upload = cloudinary.uploader.upload(qr_bytes, public_id=key, unique_filename = True, overwrite=True, folder="TagIt")
        # print(upload)
        scURL = upload['secure_url']
        
        user_qr = QR.objects.create(user=user, name=name, description=description, key=key, qr=scURL, target=target)
        user_qr.save()
        return Response({'url':scURL,'status': 'success'})
    
def scanQR(request, key):
    scanned_qr = QR.objects.filter(key=key).first()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # ip = "117.203.246.41"
    ip_response = requests.get('http://ip-api.com/json/'+ip)  
    ip_response = ip_response.json()
    location_country = ip_response['country']
    location_region = ip_response['regionName']
    location_city = ip_response['city']
    
    context = {
        "ip": ip,
        "location_country": location_country,
        "location_region": location_region,
        "location_city": location_city,
        "qr": scanned_qr.qr,
        "user": scanned_qr.user.email,
    }
    
    return render(request, '1.html', context)

# class scanQR(APIView):
#     def get(self, request, key):
#         qr = QR.objects.filter(key=key).first().qr
#     # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')    
#     # if x_forwarded_for:
#     #     ip = x_forwarded_for.split(',')[0]
#     # else:
#     #     ip = request.META.get('REMOTE_ADDR')
    
#     ip = "117.203.246.41"
#     ip_response = requests.get('http://ip-api.com/json/'+ip)  
#     ip_response = ip_response.json()
#     location_country = ip_response['country']
#     location_region = ip_response['regionName']
#     location_city = ip_response['city']
    
#     context = {
#         "ip": ip,
#         "location_country": location_country,
#         "location_region": location_region,
#         "location_city": location_city,
#         "qr": qr,
#     }
    
#     return render(request, 'info.html', context)


class get_qrs(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user=request.user
        qrs = QR.objects.filter(user=user).all()
        # qr_list = []
        # for qr in qrs:
        #     qr_list.append({
        #         "name": qr.name,
        #         "description": qr.description,
        #         "key": qr.key,
        #         "qr": qr.qr,
        #         "target": qr.target,
        #     })
        qr_list = QRSerializer(qrs, many=True)
        return Response(qr_list.data, status=status.HTTP_200_OK)