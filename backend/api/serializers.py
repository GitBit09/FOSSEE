from rest_framework import serializers
from .models import Dataset, Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'total_rows', 'summary', 'equipment']
    
    def get_summary(self, obj):
        return obj.get_summary()


class DatasetListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing datasets"""
    summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'total_rows', 'summary']
    
    def get_summary(self, obj):
        return obj.get_summary()
