import time
from copy import deepcopy
from typing import Dict

import requests
import simplejson as json
from badger_voter_sdk.aws import get_secret
from badger_voter_sdk.rich_logger import logger
from web3 import Web3

from badger_voter_sdk.constants import BADGER_VOTER_ADDRESS
from badger_voter_sdk.constants import REGION
from badger_voter_sdk.constants import SNAPSHOT_VOTE_API


class FailedToVoteException(Exception):
    pass


SNAPSHOT_DEFAULT_HEADERS = {
    'Accept': "application/json",
    'Content-Type': "application/json"
}

SNAPSHOT_TYPES_2 = {
    'EIP712Domain': [
        {'name': 'name', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
    ],
    "Vote": [
        {'name': 'from', 'type': 'address'},
        {'name': 'space', 'type': 'string'},
        {'name': 'timestamp', 'type': 'uint64'},
        {'name': 'proposal', 'type': 'bytes32'},
        {'name': 'choice', 'type': 'string'},
        {'name': 'metadata', 'type': 'string'}
    ],
}

SNAPSHOT_TYPES = {
    'EIP712Domain': [
        {'name': 'name', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
    ],
    "Vote": [
        {'name': 'from', 'type': 'address'},
        {'name': 'space', 'type': 'string'},
        {'name': 'timestamp', 'type': 'uint64'},
        {'name': 'proposal', 'type': 'string'},
        {'name': 'choice', 'type': 'string'},
        {'name': 'metadata', 'type': 'string'}
    ],
}


SNAPSHOT_DOMAIN = {
    'name': "snapshot",
    'version': "0.1.4",
}


def cast_weighed_vote(
        votes: Dict, snapshot_id: str,
        space: str, secret_id: str, secret_key: str, role_arn: str
) -> None:
    if snapshot_id.startswith("0x"):
        types = deepcopy(SNAPSHOT_TYPES_2)
    else:
        types = deepcopy(SNAPSHOT_TYPES)
    payload = {
        "domain": SNAPSHOT_DOMAIN,
        "message": {
            'from': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'space': space,
            'timestamp': int(time.time()),
            'proposal': Web3.toBytes(hexstr=snapshot_id),
            'choice': json.dumps(votes, use_decimal=True),
            'metadata': json.dumps({}),
        },
        "primaryType": 'Vote',
        "types": types,
    }
    _vote(payload, secret_id, secret_key, role_arn)


def _vote(payload: Dict, secret_id: str, secret_key: str, role_arn: str) -> None:
    private_key = get_secret(
        secret_id=secret_id,
        secret_key=secret_key,
        region_name=REGION,
        assume_role_arn=role_arn,
    )
    if not private_key:
        raise FailedToVoteException("Can't fetch private key")
    signature = sign_message(
        message=payload,
        private_key=private_key
    )
    payload.pop("primaryType")
    payload['types'].pop("EIP712Domain")
    # Convert back bytes32 to string to stringify this to json
    payload['message']['proposal'] = Web3.toHex(payload['message']['proposal'])
    response = requests.post(
        SNAPSHOT_VOTE_API,
        headers=SNAPSHOT_DEFAULT_HEADERS,
        data=json.dumps({
            'address': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'sig': signature,
            'data': payload,
        }, use_decimal=True)
    )
    if not response.ok:
        logger.error(f"Voting failed on Snapshot. Error: {response.text}")
        raise FailedToVoteException(f"Voting failed on Snapshot. Error: {response.text}")
