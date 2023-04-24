from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
import requests
from .models import QR, Scan
from .serializers import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, EmailMessage


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

from django.utils import timezone
class generateQR(APIView):
    # permission_classes = [IsAuthenticated,]

    def post(self, request):
        user=User.objects.filter(email="chandravob2003@gmail.com").first()
        print(user.phone)
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
        return Response({'url':scURL,'key':key,'status': 'success'})
    
def scanQR(request, key):
    # user=request.user
    scanned_qr = QR.objects.filter(key=key).first()
    # if (request.user and scanned_qr.user==request.user):
    #     user=request.user
    # else:
    #     user=None
    user=request.user
    
    if (request.user and scanned_qr.user==request.user):
        context = {
        'user': user,
        'key': key,
        }
        return render(request, '1.html', context)
        
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')    
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    my_date = timezone.now()
    print(my_date.tzinfo)

    # ip = "117.203.246.41"
    ip_response = requests.get('http://ip-api.com/json/'+ip)  
    ip_response = ip_response.json()
    location_country = ip_response['country']
    location_region = ip_response['regionName']
    location_city = ip_response['city']
    
    new_scan = Scan(qr=scanned_qr, location=location_city)
    new_scan.save()
    chat_link = ('https://' if request.is_secure() else 'http://') + request.META['HTTP_HOST'] + '/info/' + key
    # send_email(email,)
    
    context = {
        'user': user,
        'key': key,
        'email': scanned_qr.user.email,
        'name': scanned_qr.name,
        'location': location_city,
        'region': location_region,
        'country': location_country,
        'time': new_scan.time,
        'chat_link': chat_link,
    }
    
    send_email(context)
    
    return render(request, '1.html', context)

def send_email(context):
    sub = 'Your luggage was found'
    mess_start = 'Someone found your luggage. Here are the details:\n\n'
    mess_details = 'Location : '+context['location']+'\nRegion : '+context['region']+'\nCountry : '+context['country']+'\nTime : '+(context['time'].strftime("%d/%m/%Y, %H:%M:%S"))+'\n'
    mess_end = "Chat with your finder here : "+context['chat_link']
    mess=mess_start+mess_details+mess_end
    html_message = render_to_string('mail.html', context)
    messg=strip_tags(html_message)
    email_message = EmailMultiAlternatives(
        sub,
        messg,
        settings.EMAIL_HOST_USER,
        [context['email']]
    )
    email_message.attach_alternative(html_message, "text/html")
    print("email sent to "+context['email'])
    email_message.send()

# def scanQR(request, key):
#     qr = QR.objects.filter(key=key).first().qr
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
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        user=User.objects.filter(email="chandravob2003@gmail.com").first()
        qrs = QR.objects.filter(user=user).all().order_by('-created_at')
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
    
class getScanHistory(APIView):
    
    def post(self,request):
        user=User.objects.filter(email="chandravob2003@gmail.com").first()
        key = request.data.get('key')
        # print(key)  
        qr=QR.objects.filter(key=key).first()
        # print(qr)
        # print("hehe")
        scans = Scan.objects.filter(qr=qr).all().order_by('-time')
        # print(scans)
        # scan_list = ScanSerializer(scans, many=True)
        scan_list=[]
        for scan in scans:
            scan_list.append({
                "location": scan.location,
                "time": scan.time.strftime("%d/%m/%Y, %H:%M:%S"),
            })
        return Response(scan_list, status=status.HTTP_200_OK)
        
        
        