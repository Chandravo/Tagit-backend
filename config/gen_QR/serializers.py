from rest_framework.serializers import ModelSerializer
from .models import *

class QRSerializer(ModelSerializer):
    class Meta:
        model = QR
        fields = ('name', 'description', 'qr', 'key')


class ScanSerializer(ModelSerializer):
    class Meta:
        model = Scan
        fields = ('location','time');