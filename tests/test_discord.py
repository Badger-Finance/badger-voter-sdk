from unittest.mock import MagicMock

from discord import InvalidArgument

from badger_voter_sdk.discord import send_code_block_to_discord
from badger_voter_sdk.discord import send_message_to_discord


def test_send_code_block_to_discord_happy(mocker):
    discord = mocker.patch(
        "badger_voter_sdk.discord.Webhook.from_url",
        MagicMock()
    )
    send_code_block_to_discord(msg="message", username="BEEP BOP", url="some_url")
    assert discord.called
    assert discord.return_value.send.called


def test_send_code_block_to_discord_happy_no_url_secret_called(mocker):
    discord = mocker.patch(
        "badger_voter_sdk.discord.Webhook.from_url",
        MagicMock()
    )
    secret = mocker.patch(
        "badger_voter_sdk.discord.get_secret",
        MagicMock()
    )
    send_code_block_to_discord(msg="message", username="BEEP BOP")
    assert discord.called
    assert secret.called
    assert discord.return_value.send.called


def test_send_code_block_to_discord_bad_url(mocker):
    discord = mocker.patch(
        "badger_voter_sdk.discord.Webhook.from_url",
        side_effect=InvalidArgument()
    )
    send_code_block_to_discord(msg="message", username="BEEP BOP", url="some_url")
    assert discord.called
    assert not discord.return_value.send.called


def test_send_mesage_to_discord_happy(mocker):
    discord = mocker.patch(
        "badger_voter_sdk.discord.Webhook.from_url",
        MagicMock()
    )
    send_message_to_discord(msg="message", username="BEEP BOP", url="some_url")
    assert discord.called
    assert discord.return_value.send.called


def test_send_mesage_to_discord_happy_no_url_secret_called(mocker):
    discord = mocker.patch(
        "badger_voter_sdk.discord.Webhook.from_url",
        MagicMock()
    )
    secret = mocker.patch(
        "badger_voter_sdk.discord.get_secret",
        MagicMock()
    )
    send_message_to_discord(msg="message", username="BEEP BOP")
    assert discord.called
    assert secret.called
    assert discord.return_value.send.called


def test_send_send_mesage_to_discord_bad_url(mocker):
    discord = mocker.patch(
        "badger_voter_sdk.discord.Webhook.from_url",
        side_effect=InvalidArgument()
    )
    send_message_to_discord(msg="message", username="BEEP BOP", url="some_really_bad_url")
    assert discord.called
    assert not discord.return_value.send.called
