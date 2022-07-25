from typing import Optional

from web3 import Web3

from badger_voter_sdk.aws import get_secret
from badger_voter_sdk.constants import ETHNODEURL_SECRET_ID
from badger_voter_sdk.constants import ETHNODEURL_SECRET_KEY


class EthNodeNotFound(Exception):
    pass


def get_web3(node_url: Optional[str] = "") -> Web3:
    """
    Returns Web3 instance connected to RPC node
    """
    ethnode = node_url or get_secret(
        secret_id=ETHNODEURL_SECRET_ID,
        secret_key=ETHNODEURL_SECRET_KEY,
    )
    if not ethnode:
        raise EthNodeNotFound("ETHNODEURL not found")
    return Web3(Web3.HTTPProvider(ethnode))
