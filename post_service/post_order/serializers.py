from rest_framework import serializers
from post_order.models import Client, PostOrder, Message


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('id',)


class PostOrderSerializer(serializers.ModelSerializer):

    messages_sent = serializers.IntegerField(
        label='Число отправленных сообщений', 
        required=False)
    
    messages_error = serializers.IntegerField(
        label='Число отправленных сообщений отправленных с ошибкой', 
        required=False)
    
    messages_processing = serializers.IntegerField(
        label='Число обрабатываемых сообщений',
        required=False)
    
    messages_expired = serializers.IntegerField(
        label='Число просроченных сообщений',
        required=False)

    class Meta:
        model = PostOrder
        fields = '__all__'
        read_only_fields = ('id', 'messages_sent', 'messages_error', 
                            'messages_processing', 'messages_expired')
