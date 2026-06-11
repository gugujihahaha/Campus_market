from goods.models import Notification


def send_notification(recipient, type_, title, content, link="", sender=None):
    """创建一条通知"""
    return Notification.objects.create(
        recipient=recipient,
        sender=sender,
        type=type_,
        title=title,
        content=content,
        link=link,
    )
