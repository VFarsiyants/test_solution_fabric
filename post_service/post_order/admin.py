from django.contrib import admin
from .models import Client, Message, PostOrder


admin.site.register(Client)
admin.site.register(Message)
admin.site.register(PostOrder)
