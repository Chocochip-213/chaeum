from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = Resume
        fields = ['id', 'file', 'file_name', 'status', 'uploaded_at']
        read_only_fields = ['id', 'file_name', 'status', 'uploaded_at']

    def create(self, validated_data):
        validated_data.pop('file', None)
        return super().create(validated_data)