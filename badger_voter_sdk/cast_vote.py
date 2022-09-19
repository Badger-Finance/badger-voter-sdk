import time
from copy import deepcopy
from typing import Dict

import requests
import simplejson as json
from badger_voter_sdk.aws import get_secret
from badger_voter_sdk.constants import SnapshotType
from badger_voter_sdk.json_logger import logger
from web3 import Web3

from badger_voter_sdk.constants import BADGER_VOTER_ADDRESS
from badger_voter_sdk.constants import REGION
from badger_voter_sdk.constants import SNAPSHOT_VOTE_API
from badger_voter_sdk.utils import sign_message


class FailedToVoteException(Exception):
    pass


SNAPSHOT_DEFAULT_HEADERS = {
    'Accept': "application/json",
    'Content-Type': "application/json"
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

SNAPSHOT_SINGLE_CHOICE_TYPES = {
    'EIP712Domain': [
        {'name': 'name', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
    ],
    "Vote": [
        {'name': 'from', 'type': 'address'},
        {'name': 'space', 'type': 'string'},
        {'name': 'timestamp', 'type': 'uint64'},
        {'name': 'proposal', 'type': 'string'},
        {'name': 'choice', 'type': 'uint32'},
        {'name': 'metadata', 'type': 'string'}
    ],
}

SNAPSHOT_SINGLE_CHOICE_TYPES_2 = {
    'EIP712Domain': [
        {'name': 'name', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
    ],
    "Vote": [
        {'name': 'from', 'type': 'address'},
        {'name': 'space', 'type': 'string'},
        {'name': 'timestamp', 'type': 'uint64'},
        {'name': 'proposal', 'type': 'bytes32'},
        {'name': 'choice', 'type': 'uint32'},
        {'name': 'metadata', 'type': 'string'}
    ],
}


SNAPSHOT_DOMAIN = {
    'name': "snapshot",
    'version': "0.1.4",
}


def cast_weighed_vote(
        votes: Dict, snapshot_id: str, web3: Web3,
        space: str, secret_id: str, secret_key: str, role_arn: str
) -> None:
    """
    Cast weighed vote choices for selected space on Snapshot
    """
    snapshot_type = (
        SnapshotType.TYPE_2.value if snapshot_id.startswith('0x') else SnapshotType.TYPE_1.value
    )
    if snapshot_type == SnapshotType.TYPE_2:
        types = deepcopy(SNAPSHOT_TYPES_2)
    else:
        types = deepcopy(SNAPSHOT_TYPES)
    payload = {
        "domain": SNAPSHOT_DOMAIN,
        "message": {
            'from': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'space': space,
            'timestamp': int(time.time()),
            'proposal': (
                Web3.toBytes(hexstr=snapshot_id) if snapshot_type == SnapshotType.TYPE_2
                else snapshot_id
            ),
            'choice': json.dumps(votes, use_decimal=True),
            'metadata': json.dumps({}),
        },
        "primaryType": 'Vote',
        "types": types,
    }
    _vote(snapshot_type, payload, secret_id, secret_key, role_arn, web3)


def cast_single_choice_vote(
        choice: int, snapshot_id: str, web3: Web3, space: str,
        secret_id: str, secret_key: str, role_arn: str
) -> None:
    """
    Single choice voting function needed for voting on gauges etc
    """
    snapshot_type = (
        SnapshotType.TYPE_2.value if snapshot_id.startswith('0x') else SnapshotType.TYPE_1.value
    )
    if snapshot_type == SnapshotType.TYPE_2:
        types = deepcopy(SNAPSHOT_SINGLE_CHOICE_TYPES_2)
    else:
        types = deepcopy(SNAPSHOT_SINGLE_CHOICE_TYPES)
    payload = {
        "domain": SNAPSHOT_DOMAIN,
        "message": {
            'from': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'space': space,
            'timestamp': int(time.time()),
            'proposal': (
                Web3.toBytes(hexstr=snapshot_id) if snapshot_type == SnapshotType.TYPE_2
                else snapshot_id
            ),
            'choice': int(choice),
            'metadata': json.dumps({}),
        },
        "primaryType": 'Vote',
        "types": types,
    }
    _vote(snapshot_type, payload, secret_id, secret_key, role_arn, web3)


def _vote(
        snapshot_type: SnapshotType, payload: Dict, secret_id: str, secret_key: str, role_arn: str,
        web3: Web3,
) -> None:
    private_key = get_secret(
        secret_id=secret_id,
        secret_key=secret_key,
        region_name=REGION,
        assume_role_arn=role_arn,
    )
    if not private_key:
        raise FailedToVoteException("Can't fetch private key")
    signature = sign_message(
        web3,
        snapshot_type,
        message=payload,
        private_key=private_key
    )
    payload.pop("primaryType")
    payload['types'].pop("EIP712Domain")
    if snapshot_type == SnapshotType.TYPE_2:
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
