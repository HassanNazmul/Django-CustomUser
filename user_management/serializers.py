from rest_framework import serializers
from user_management.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'full_name', 'is_student', 'is_admin', 'is_staff', 'is_active',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            # If the user is a superuser, only display email, full_name, and is_superuser
            return {
                'id': instance.id,
                'email': representation['email'],
                'full_name': representation['full_name'],
                'is_superuser': instance.is_superuser
            }
        return representation


class CustomUserRestrictedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'full_name', 'is_student', 'is_admin', 'is_staff', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'email', 'date_joined']

    def update(self, instance, validated_data):
        # Prevent email from being updated
        validated_data.pop('email', None)
        return super().update(instance, validated_data)
