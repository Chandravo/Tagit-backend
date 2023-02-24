from rest_framework.serializers import ModelSerializer
from .models import QR

class QRSerializer(ModelSerializer):
    class Meta:
        model = QR
        fields = ('name', 'description', 'qr')