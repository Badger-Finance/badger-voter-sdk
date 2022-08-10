from typing import Optional

from discord import InvalidArgument
from discord import RequestsWebhookAdapter
from discord import Webhook

from badger_voter_sdk.aws import get_secret
from badger_voter_sdk.rich_logger import logger


def send_code_block_to_discord(
    msg: str, username: str, url: Optional[str] = None,
    webhook_secret_id: Optional[str] = '',
    webhook_secret_key: Optional[str] = '',
):
    if not url:
        url = get_secret(
            secret_id=webhook_secret_id,
            secret_key=webhook_secret_key,
        )
    try:
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
    except InvalidArgument:
        logger.error("Discord Webhook URL is not configured")
        return
    msg = f"```\n{msg}\n```"
    webhook.send(username=username, content=msg)


def send_message_to_discord(
    msg: str,
    username: str,
    url: Optional[str] = None,
    webhook_secret_id: Optional[str] = '',
    webhook_secret_key: Optional[str] = '',
) -> None:
    if not url:
        url = get_secret(
            secret_id=webhook_secret_id,
            secret_key=webhook_secret_key,
        )
    try:
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
    except InvalidArgument:
        logger.error("Discord Webhook URL is not configured")
        return
    webhook.send(content=msg, username=username)
