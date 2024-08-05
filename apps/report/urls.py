from django.urls import path
from .views import (
    UserIncidentListAPIView, IncidentCreateView,
    IncidentUpdateView
)

app_name = "report"

urlpatterns = [
    path('user/incidents/list/', UserIncidentListAPIView.as_view()),
    path('user/incidents/create/', IncidentCreateView.as_view()),
    path('user/incidents/update/<int:pk>/', IncidentUpdateView.as_view(), name='incident-update'),
]