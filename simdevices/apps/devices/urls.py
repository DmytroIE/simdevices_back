from django.urls import path
from .views import DeviceListCreate, DeviceRetrieveUpdateDestroy

urlpatterns = [
    path('', DeviceListCreate.as_view()),
    path('<int:pk>/', DeviceRetrieveUpdateDestroy.as_view()),
]