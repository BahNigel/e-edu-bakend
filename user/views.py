# views.py

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer

class LoggedInUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
