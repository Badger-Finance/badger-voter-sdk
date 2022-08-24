from copy import deepcopy
from unittest.mock import MagicMock

import pytest

from badger_voter_sdk.collectors.snapshot_collectors import get_gauge_weight_snapshot
from badger_voter_sdk.collectors.snapshot_collectors import get_snapshot_by_id
from badger_voter_sdk.collectors.snapshot_collectors import get_voters
from tests.test_data.snapshot_data import ACTIVE_PROPOSAL_DATA
from tests.test_data.snapshot_data import SNAPSHOT_DATA_BY_ID
from tests.test_data.snapshot_data import STALE_VOTES_SNAPSHOT

TESTED_VOTER_ADDRESS = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"


def test_get_voters_happy(mocker):
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                side_effect=[STALE_VOTES_SNAPSHOT, {}],
            )
        )
    )
    voters = get_voters(
        snapshot_id="0x9a21d743bbdf54f2505f022564686c0431d5e95771318f2b67c807960ae4bd8d"
    )
    assert voters[TESTED_VOTER_ADDRESS] == {
        "10": 34.02,
        "38": 40.26,
        "46": 17.21,
        "72": 8.51
    }


def test_get_voters_happy_empty(mocker):
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_voters(
        snapshot_id="0x9a21d743bbdf54f2505f022564686c0431d5e95771318f2b67c807960ae4bd8d"
    )


def test_get_snapshot_by_id(mocker):
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=SNAPSHOT_DATA_BY_ID,
            )
        )
    )
    snapshot = get_snapshot_by_id(
        "0x632726577e9c186a8827311b8702dcfd98f26376237b9715e64eafa61d6d7672"
    )
    assert snapshot['title'] == SNAPSHOT_DATA_BY_ID['proposals'][0]['title']
    assert snapshot['state'] == "closed"


def test_get_snapshot_by_id_empty_res(mocker):
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_snapshot_by_id(
        "0x632726577e9c186a8827311b8702dcfd98f26376237b9715e64eafa61d6d7672"
    )


def test_get_gauge_weight_snapshot_happy(mocker):
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=ACTIVE_PROPOSAL_DATA,
            )
        )
    )
    web3 = MagicMock(eth=MagicMock(
        getBlock=MagicMock(
            return_value={'timestamp': 1658390415}
        )
    ))
    result = get_gauge_weight_snapshot(web3, space='aurafinance.eth')
    assert result['title'] == "Gauge Weight for Week of 21st July 2022"
    assert result['state'] == "active"
    assert result['space'] == {'id': 'aurafinance.eth', 'name': 'Aura Finance'}
    assert result['strategies'] is not None


def test_get_gauge_weight_snapshot_empty_res(mocker):
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_gauge_weight_snapshot(web3=MagicMock(), space="aurafinance.eth")


@pytest.mark.parametrize('timestamp', [1648684815, 2948684815])
def test_get_gauge_weight_snapshot_no_match(mocker, timestamp):
    """
    timestamp is way off from proposal start and end times
    """
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=ACTIVE_PROPOSAL_DATA,
            )
        )
    )
    web3 = MagicMock(eth=MagicMock(
        getBlock=MagicMock(
            return_value={'timestamp': timestamp}
        )
    ))

    assert not get_gauge_weight_snapshot(web3=web3, space="aurafinance.eth")


def test_get_gauge_weight_snapshot_no_active(mocker):
    data = deepcopy(ACTIVE_PROPOSAL_DATA)
    data['proposals'][0]['state'] = "closed"
    mocker.patch(
        'badger_voter_sdk.collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=data,
            )
        )
    )
    web3 = MagicMock(eth=MagicMock(
        getBlock=MagicMock(
            return_value={'timestamp': 1657159210}
        )
    ))

    assert not get_gauge_weight_snapshot(web3=web3, space="aurafinance.eth")
