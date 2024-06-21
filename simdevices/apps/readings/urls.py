from django.urls import path,register_converter
from .views import ReadingListCreate, ReadingRetrieveUpdateDestroy
from .converters import DateTimeToUnixConverter

register_converter(DateTimeToUnixConverter, 'datetime')


urlpatterns = [
    path('', ReadingListCreate.as_view()),
    path('<datetime:pk>/', ReadingRetrieveUpdateDestroy.as_view()),
]