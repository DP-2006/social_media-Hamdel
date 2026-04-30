# apps/accounts/tasks.py

from celery import shared_task
from core.services.sms_service import get_sms_provider
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_sms_async(phone: str, code: str):
    provider = get_sms_provider()
    success = provider.send(phone, code)
    
    if success:
        logger.info(f"SMS sent to {phone}")
    else:
        logger.error(f"Failed to send SMS to {phone}")
    
    return success

@shared_task
def send_bale_async(chat_id: str, code: str):
    from apps.accounts.bale_webhook import send_bale_message
    return send_bale_message(chat_id, f"کد تأیید: {code}")