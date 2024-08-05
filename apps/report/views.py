from rest_framework import generics, permissions
from .models import IncidentReport
from apps.report.serializer import IncidentReportSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner

class UserIncidentListAPIView(generics.ListAPIView):
    """ List of incident created by a user API.

    API is also used to search for an incident by incident id. 
    """
    serializer_class = IncidentReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = IncidentReport.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = IncidentReport.objects.filter(user=user)
        
        incident_id = self.request.query_params.get('incident_id', None)
        if incident_id is not None:
            queryset = queryset.filter(incident_id__icontains=incident_id)
        
        return queryset
    
class IncidentCreateView(generics.CreateAPIView):
    """Create a new incident API."""

    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IncidentUpdateView(generics.UpdateAPIView):
    """ Update a incident API.
    
    If the incident's status is closed it can't be updated.
    """

    queryset = IncidentReport.objects.all()
    serializer_class = IncidentReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return IncidentReport.objects.filter(user=self.request.user)