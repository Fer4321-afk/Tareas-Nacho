from rest_framework import serializers
from .models import ErrorReport
from datetime import datetime

class StatusSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100)
    date = serializers.DateTimeField()

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorReport
        fields = ['id', 'code', 'description', 'date']