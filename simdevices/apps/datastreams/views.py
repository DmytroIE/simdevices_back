from django.db.models import ProtectedError
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Datastream
from .serializers import DatastreamSerializer


class DatastreamListCreate(generics.ListCreateAPIView):
    queryset = Datastream.objects.all()
    serializer_class = DatastreamSerializer


class DatastreamRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Datastream.objects.all()
    serializer_class = DatastreamSerializer

    def perform_destroy(self, instance):
        print('perform destroy')
        task = getattr(instance, 'task', None)
        try:
            super().perform_destroy(instance)
        except ProtectedError:
            raise
        if task:
            task.enabled = False
            task.save()
            task.delete()
            print('task is deleted first')

    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError as exception:
            response_msg = {
                'error': {'type': str(type(exception)), 'message': 'The instance has dependencies and cannot be deleted'},
            }
            return Response(response_msg, status=status.HTTP_400_BAD_REQUEST)
            


# https://stackoverflow.com/questions/44229783/catch-protected-error-and-show-its-message-to-the-user-instead-of-bare-500-code