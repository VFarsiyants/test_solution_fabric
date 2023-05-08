from .tasks import start_posting
from post_order.models import PostOrder


def create_posting_task(post_order: PostOrder):
    start_time = post_order.start_time
    end_time = post_order.end_time
    start_posting.apply_async(
        args=[post_order.id], 
        eta=start_time, 
        expires=end_time
    )
