from rest_framework import viewsets

from fba.models.hazard_event import HazardEvent
from fba.serializers.hazard_event import HazardEventSerializer


class HazardEventAPI(viewsets.ModelViewSet):
    """API for listing hazard event"""

    queryset = HazardEvent.objects.all()
    serializer_class = HazardEventSerializer
