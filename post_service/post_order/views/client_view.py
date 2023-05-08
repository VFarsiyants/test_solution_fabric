from rest_framework.viewsets import ModelViewSet

from post_order.serializers import ClientSerializer
from post_order.models import Client


class ClientViewSet(ModelViewSet):
    """Viewset to create, edit, delete client instances
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
