import time
from unittest.mock import MagicMock

import pytest

from badger_voter_sdk.constants import SnapshotType
from badger_voter_sdk.utils import sign_message


@pytest.mark.parametrize(
    'snap_type',
    [SnapshotType.TYPE_1.value, SnapshotType.TYPE_2.value]
)
def test_sign_message(snap_type):
    web3 = MagicMock(eth=MagicMock(
        account=MagicMock(
            sign_message=MagicMock(return_value={
                'signature': b"\x9d\xa7\x12P\xaf\xd0\xb6'\
                    x9b\x06\xc5\xfd/\xb9\x83y'\xb3\xff\x9e\x05\xcf"}
            )
        )
    ))

    msg = {
        "domain": {
            "chainId": 1,
            "name": 'snapshot',
            "verifyingContract": '0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC',
            "version": '0.1.4',
        },
        "message": {
            'from': "0x12d8E12e981be773cb777Be342a528228b3c7661",
            'space': "unknown.eth",
            'timestamp': int(time.time()),
            'proposal': "QmetYVgwr8MXEBVg4gHNNK2D5Jre18vtJgC14VhDirh4VJ",
            'choice': "pogger",
            'metadata': "",
        },
        "primaryType": 'Vote',
        "types": {
            'EIP712Domain': [
                {'name': 'name', 'type': 'string'},
                {'name': 'version', 'type': 'string'},
                {'name': 'chainId', 'type': 'uint256'},
                {'name': 'verifyingContract', 'type': 'address'},
            ],
            "Vote": [
                {'name': 'from', 'type': 'address'},
                {'name': 'space', 'type': 'string'},
                {'name': 'timestamp', 'type': 'uint64'},
                {'name': 'proposal', 'type': 'string'},
                {'name': 'choice', 'type': 'string'},
                {'name': 'metadata', 'type': 'string'}
            ],
        },
    }
    signature = sign_message(
        web3=web3,
        snapshot_type=snap_type,
        message=msg,
        # Some random pk
        private_key="123"
    )
    assert signature == '9da71250afd0b62720202020202020202020202020202' \
                        '0202020202078396206c5fd2fb9837927b3ff9e05cf'
