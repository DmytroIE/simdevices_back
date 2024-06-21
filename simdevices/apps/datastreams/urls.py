from django.urls import path
from .views import DatastreamListCreate, DatastreamRetrieveUpdateDestroy

urlpatterns = [
    path('', DatastreamListCreate.as_view()),
    path('<int:pk>/', DatastreamRetrieveUpdateDestroy.as_view()),
]