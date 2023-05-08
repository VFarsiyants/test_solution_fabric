from django.db import models


class Message(models.Model):

    status_choises = (
        ('processing', 'Отправка сообщения'),
        ('sent', 'Отправлено'),
        ('error', 'Ошибка'),
        ('expired', 'Доставка просрочена')
    )

    created_time = models.DateTimeField(
        verbose_name='Дата и время создания (отправки)',
        auto_now=True
    )
    status = models.CharField(max_length=10, choices=status_choises)

    post_order = models.ForeignKey(
        'post_order.PostOrder', 
        related_name='MESSAGE_POSTORDER',
        on_delete=models.PROTECT)
    
    client = models.ForeignKey(
        'post_order.Client',
        related_name='MESSAGE_CLIENT',
        on_delete=models.PROTECT
    )
