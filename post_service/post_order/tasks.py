import asyncio
import aiohttp
from datetime import datetime
import json
import pytz

from asgiref.sync import sync_to_async
from celery.signals import task_revoked
from django.conf import settings
from django.db.models import Q

from post_service.celery import app
from post_order.models import Message, PostOrder, Client


async def _post_message(url, session, message, text, end_time):
    """Function to process request to an API
    """
    payload = {
        "id": message.client_id,
        "phone": str(message.client.phone_number),
        "text": text
    }
    now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    if now > end_time:
        # if cooritine was taken in action after celery started to do the task
        # and it's expired according order, we should not send any requests 
        # anymore
        await _update_message_status(message, 'expired')
        return
    timeout = (end_time - now).total_seconds()
    try:
        response = await asyncio.wait_for(
            session.post(
                url, 
                data=json.dumps(payload),
                allow_redirects=True
            ),
            timeout=timeout
        )
        status = response.status
        message_status = 'sent' if status == 200 else 'error'
        await _update_message_status(message, message_status)
    except (asyncio.TimeoutError, aiohttp.ClientConnectorError) as e:
        # If we don't received response from API and order is expired
        await _update_message_status(message, 'expired')


async def _execute_post_order(order: PostOrder, messages):
    """Function to start posting all request to API for desired order
    """
    tasks = []
    text = order.message_text
    end_time = order.end_time

    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers={
                'Authorization': f'Bearer {settings.ACCESS_TOKEN}'
            }) as session:
        for message in messages:
            url = f"{settings.API_URL}/send/{message.client.id}"
            task = asyncio.create_task(
                _post_message(url, session, message, text, end_time))
            tasks.append(task)
        await asyncio.gather(*tasks)


@sync_to_async
def _update_message_status(message, status):
    """updating status of message in db
    """
    message.status = status
    message.save()


@app.task
def start_posting(post_order_id):
    order = PostOrder.objects.get(pk=post_order_id)
    filter_value = order.filter_property
    condition = Q(mobile_code=int(filter_value)) if filter_value.isdigit() \
        else Q(tag=filter_value)
    clients = list(Client.objects.filter(condition))
    messages = []
    for client in clients:
        message = Message.objects.create(
            post_order=order,
            client=client,
            status='processing'
        )
        messages.append(message)
    asyncio.run(_execute_post_order(order, messages))


@task_revoked.connect
def handle_task_revoked(sender=None, request=None, expired=None, **kwargs):
    if expired and sender.name == 'post_order.tasks.start_posting':
        order_id = request.args[0]
        print(f'post_order with id {order_id} is expired, '
              f'messages won\'t be delivered')
