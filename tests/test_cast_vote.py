import json
from unittest.mock import MagicMock

import pytest
import responses

from badger_voter_sdk.cast_vote import FailedToVoteException
from badger_voter_sdk.cast_vote import cast_single_choice_vote
from badger_voter_sdk.cast_vote import cast_weighed_vote
from badger_voter_sdk.constants import SNAPSHOT_VOTE_API


@responses.activate
@pytest.mark.parametrize(
    'voting_executable',
    [cast_weighed_vote, cast_single_choice_vote]
)
@pytest.mark.parametrize(
    'snapshot',
    # Normal snapshot; snapshot id as bytes
    ["bafkreie7zi37m4uct4u6odwfddudgm7whkkv74msxffuzztgxeaz7om7d4",
     "0x2445e521270db2ef0c3f6fae8903c5a753d48e112928507ca1d479a3b7b90bfd"]
)
def test_cast_vote_happy(mocker, voting_executable, snapshot):
    mocker.patch(
        "badger_voter_sdk.cast_vote.get_secret",
        return_value="private_key"
    )
    mocker.patch(
        "badger_voter_sdk.cast_vote.sign_message",
        return_value="signed_message"
    )
    responses.add(
        responses.POST,
        SNAPSHOT_VOTE_API,
        json={}, status=200
    )
    voting_executable(
        {'1': 1},
        snapshot_id=snapshot, space="cvx.eth",
        web3=MagicMock(), secret_id="", secret_key="", role_arn="",
    ) if voting_executable is cast_weighed_vote else voting_executable(
        1,
        snapshot_id="123", space="cvx.eth",
        web3=MagicMock(), secret_id="", secret_key="", role_arn="",
    )
    body = json.loads(responses.calls[0].request.body)
    assert 'address' in body.keys()
    assert 'sig' in body.keys()
    assert 'data' in body.keys()


@responses.activate
@pytest.mark.parametrize(
    'voting_executable',
    [cast_weighed_vote, cast_single_choice_vote]
)
def test_cast_vote_no_pk(mocker, voting_executable):
    """
    When no pk secret - should raise exc
    """
    mocker.patch(
        "badger_voter_sdk.cast_vote.get_secret",
        return_value=None
    )
    mocker.patch(
        "badger_voter_sdk.cast_vote.sign_message",
        return_value="signed_message"
    )
    responses.add(
        responses.POST,
        SNAPSHOT_VOTE_API,
        json={}, status=200
    )
    with pytest.raises(FailedToVoteException) as exc:
        voting_executable(
            {'1': 1},
            snapshot_id="123", space="cvx.eth",
            web3=MagicMock(), secret_id="", secret_key="", role_arn="",
        ) if voting_executable is cast_weighed_vote else voting_executable(
            1,
            snapshot_id="123", space="cvx.eth",
            web3=MagicMock(), secret_id="", secret_key="", role_arn="",
        )
    assert str(exc.value) == "Can't fetch private key"


@responses.activate
@pytest.mark.parametrize(
    'voting_executable',
    [cast_weighed_vote, cast_single_choice_vote]
)
def test_cast_vote_error(mocker, voting_executable):
    """
    When vote didn't happen - raise exc
    """
    mocker.patch(
        "badger_voter_sdk.cast_vote.get_secret",
        return_value="pk"
    )
    mocker.patch(
        "badger_voter_sdk.cast_vote.sign_message",
        return_value="signed_message"
    )
    responses.add(
        responses.POST,
        SNAPSHOT_VOTE_API,
        json={}, status=500
    )
    with pytest.raises(FailedToVoteException) as exc:
        voting_executable(
            {'1': 1},
            snapshot_id="123", space="cvx.eth",
            web3=MagicMock(), secret_id="", secret_key="", role_arn="",
        ) if voting_executable is cast_weighed_vote else voting_executable(
            1,
            snapshot_id="123", space="cvx.eth",
            web3=MagicMock(), secret_id="", secret_key="", role_arn="",
        )
    assert str(exc.value) == "Voting failed on Snapshot. Error: {}"
