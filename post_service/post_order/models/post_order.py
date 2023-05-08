from django.db import models


class PostOrder(models.Model):
    start_time = models.DateTimeField(
        verbose_name='Дата и вермя запуска расыылки'
    )
    message_text = models.CharField(
        max_length=300, 
        verbose_name='Текст сообщения для доставки клиенту'
    )

    filter_property = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Фильтр свойств клиентов для доставки '
                     '(тег или код мобильного оператора)'
    )
    
    end_time = models.DateTimeField(
        verbose_name='Дата времени окончания рассылки'
    )
