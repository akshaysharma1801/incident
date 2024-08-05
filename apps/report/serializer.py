from rest_framework import serializers
from .models import IncidentReport
from apps.account.serializer import UserDetailSerializer

class IncidentReportSerializer(serializers.ModelSerializer):
    """ Create read update Incident serializer. """

    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = IncidentReport
        fields = '__all__'
        read_only_fields = ['incident_id', 'incident_reported_date', 'user']

    def update(self, instance, validated_data):
        if instance.status == "Closed":
            raise serializers.ValidationError('Closed status cannot be updated.')
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance