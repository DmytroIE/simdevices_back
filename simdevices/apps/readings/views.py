from .models import Reading
from .serializers import ReadingSerializer
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import datetime


class ReadingListCreate(generics.ListCreateAPIView):
    # queryset = Reading.objects.all()
    serializer_class = ReadingSerializer

    def get_queryset(self):
        from_ = self.request.query_params.get('from')
        to_ = self.request.query_params.get('to')
        if from_ is None and to_ is None:
            return Reading.objects.all()
        try:
            if from_ is not None and to_ is None:
                miliseconds = int(from_)
                from_dt = datetime.fromtimestamp(miliseconds / 1000.0)
                return Reading.objects.filter(timestamp__gte = from_dt)
            elif from_ is None and to_ is not None:
                miliseconds = int(to_)
                to_dt = datetime.fromtimestamp(miliseconds / 1000.0)
                return Reading.objects.filter(timestamp__lte = to_dt) # it works as lt!!!
                # maybe it is necessary to use a filter https://django-filter.readthedocs.io/en/main/ref/filters.html#isodatetimefromtorangefilter
            else:
                miliseconds = int(from_)
                from_dt = datetime.fromtimestamp(miliseconds / 1000.0)
                miliseconds = int(to_)
                to_dt = datetime.fromtimestamp(miliseconds / 1000.0)
                return Reading.objects.filter(timestamp__lte = to_dt).filter(timestamp__gte = from_dt)
        except:
            return Reading.objects.all()

    # def post(self, request):
    #     #print(type(request.data))
    #     print(request.data)
    #     return Response('OK', status=status.HTTP_201_CREATED)


class ReadingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reading.objects.all()
    serializer_class = ReadingSerializer

    # def put(self, request, pk):
    #     print(request.data)
    #     print(pk)
    #     print(type(pk))
    #     return Response('OK', status=status.HTTP_200_OK)
    

    
# https://stackoverflow.com/questions/54790821/put-and-delete-request-in-django-rest-framework
