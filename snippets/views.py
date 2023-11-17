from rest_framework import mixins, renderers
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import permissions, generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


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

@api_view(['GET'])
def api_root(request, format=None):
   return Response({
       'users': reverse('user-list', request=request, format=format),
       'snippets': reverse('snippet-list', request=request, format=format)
   })


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

class SnippetHighlight(generics.GenericAPIView):
   queryset = Snippet.objects.all()
   renderer_classes = [renderers.StaticHTMLRenderer]

   def get(self, request, **kwargs):
       snippet = self.get_object()
       return Response(snippet.highlighted)
