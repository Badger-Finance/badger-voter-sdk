from typing import Dict
from typing import Mapping
from typing import Union

from eth_account._utils.structured_data.hashing import hash_domain  # noqa
from eth_account._utils.structured_data.hashing import hash_message as hash_eip712_message  # noqa
from eth_account._utils.structured_data.hashing import load_and_validate_structured_message  # noqa
from eth_account._utils.structured_data.validation import validate_structured_data  # noqa
from eth_account.messages import SignableMessage
from eth_account.messages import encode_structured_data
from eth_utils.curried import to_text
from hexbytes import HexBytes
from web3 import Web3

from badger_voter_sdk.constants import SnapshotType


def _encode_structured_data(
        primitive: Union[bytes, int, Mapping] = None,
        *,
        hexstr: str = None,
        text: str = None) -> SignableMessage:
    """
    TODO: this is copypasted code from newer eth-account library that we cannot use it since our
    TODO: web3 version doesn't support it. Migrate to newer v ASAP once web3 is released
    """
    if isinstance(primitive, Mapping):
        validate_structured_data(primitive)
        structured_data = primitive
    else:
        message_string = to_text(primitive, hexstr=hexstr, text=text)
        structured_data = load_and_validate_structured_message(message_string)
    return SignableMessage(
        HexBytes(b'\x01'),
        hash_domain(structured_data),
        hash_eip712_message(structured_data),
    )


def sign_message(web3: Web3, snapshot_type: str, message: Dict, private_key: str) -> str:
    """
    EIP712 message signing
    """
    if snapshot_type == SnapshotType.TYPE_2:
        encoded_data = _encode_structured_data(primitive=message)
    else:
        encoded_data = encode_structured_data(primitive=message)
    signed_message = web3.eth.account.sign_message(encoded_data, private_key)
    return signed_message['signature'].hex()
