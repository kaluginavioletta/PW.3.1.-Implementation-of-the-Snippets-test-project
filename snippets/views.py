from rest_framework import mixins
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class SnippetList(generics.ListCreateAPIView):
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   def perform_create(self, serializer):
       serializer.save(owner=self.request.user)

   def get(self, request, *args, **kwargs):
       return self.list(request, *args, **kwargs)

   def post(self, request, *args, **kwargs):
       return self.create(request, *args, **kwargs)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

   def get(self, request, *args, **kwargs):
       return self.retrieve(request, *args, **kwargs)

   def put(self, request, *args, **kwargs):
       return self.update(request, *args, **kwargs)

   def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)

from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import UserSerializer

class UserList(generics.ListAPIView):
   queryset = User.objects.all()
   serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
   queryset = User.objects.all()
   serializer_class = UserSerializer
