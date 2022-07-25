import pytest

from badger_voter_sdk.web3 import EthNodeNotFound
from badger_voter_sdk.web3 import get_web3


def test_web3():
    web3 = get_web3("some_node_url")
    assert not web3.isConnected()


def test_web3_no_env_var(mocker):
    mocker.patch("badger_voter_sdk.web3.get_secret", return_value=None)
    with pytest.raises(EthNodeNotFound):
        get_web3()
