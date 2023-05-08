from rest_framework import serializers
from post_order.models import Client, PostOrder, Message


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('id',)


class PostOrderSerializer(serializers.ModelSerializer):

    messages_sent = serializers.IntegerField(
        label='Число отправленных сообщений')
    
    messages_error = serializers.IntegerField(
        label='Число отправленных сообщений отправленных с ошибкой')
    
    messages_processing = serializers.IntegerField(
        label='Число обрабатываемых сообщений')
    
    messages_expired = serializers.IntegerField(
        label='Число просроченных сообщений')

    class Meta:
        model = PostOrder
        fields = '__all__'
        read_only_fields = ('id', 'messages_sent', 'messages_error', 
                            'messages_processing', 'messages_expired')
