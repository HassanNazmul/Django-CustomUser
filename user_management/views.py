from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from user_management.models import CustomUser
from user_management.serializers import CustomUserSerializer, CustomUserRestrictedUpdateSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the ability to list, retrieve, create, update, and delete users.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Restrict listing to admin and staff users only
        if not self.request.user.is_admin and not self.request.user.is_staff:
            # Allow students to only see their own information
            return CustomUser.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    def get_serializer_class(self):
        # Use a serializer that restricts email update for students
        if self.action in ['update', 'partial_update'] and not (
                self.request.user.is_admin or self.request.user.is_staff):
            return CustomUserRestrictedUpdateSerializer
        return CustomUserSerializer

    def perform_create(self, serializer):
        # Allow only admin and staff users to create users
        if not (self.request.user.is_admin or self.request.user.is_staff):
            raise ValidationError("You do not have permission to create a user.")
        serializer.save()

    def perform_update(self, serializer):
        # Allow only admin and staff users to update users, but allow students to update their own details
        if not (self.request.user.is_admin or self.request.user.is_staff):
            if self.request.user != serializer.instance:
                raise ValidationError("You do not have permission to update this user.")
        serializer.save()

    def perform_destroy(self, instance):
        # Allow only admin and staff users to delete users
        if not (self.request.user.is_admin or self.request.user.is_staff):
            raise ValidationError("You do not have permission to delete a user.")
        instance.delete()
