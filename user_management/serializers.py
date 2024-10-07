from rest_framework import serializers

from user_management.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'is_student', 'is_admin', 'is_active', 'date_joined']
