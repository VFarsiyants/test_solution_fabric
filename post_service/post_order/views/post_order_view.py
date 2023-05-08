from django.db.models import Count, Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from post_order.models import PostOrder
from post_order.serializers import PostOrderSerializer
from post_order.services import create_posting_task


class PostOrderViewSet(ModelViewSet):
    """Viewset to create, update, delete PostOrderInstances"""
    queryset = PostOrder.objects.all()
    serializer_class = PostOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        #creating task for celery for new PostOrder
        create_posting_task(serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    def get_queryset(self):
        q = super().get_queryset()
        return self.annotate_queryset(q)
    
    def annotate_queryset(self, queryset):
        return queryset.annotate(
            messages_sent=Count(
                'MESSAGE_POSTORDER__id',
                filter=Q(MESSAGE_POSTORDER__status='sent')
            ),
            messages_error=Count(
                'MESSAGE_POSTORDER__id',
                filter=Q(MESSAGE_POSTORDER__status='error')
            ),
            messages_processing=Count(
                'MESSAGE_POSTORDER__id',
                filter=Q(MESSAGE_POSTORDER__status='processing')
            ),
            messages_expired=Count(
                'MESSAGE_POSTORDER__id',
                filter=Q(MESSAGE_POSTORDER__status='expired')
            ),
        )
