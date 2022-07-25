import responses

from badger_voter_sdk.collectors.api_collectors import get_scores
from badger_voter_sdk.constants import BADGER_VOTER_ADDRESS
from badger_voter_sdk.constants import SNAPSHOT_SCORES_URL

TEST_SNAPSHOT_ID = "0x9a21d743bbdf54f2505f022564686c0431d5e95771318f2b67c807960ae4bd8d"


@responses.activate
def test_get_scores_happy():
    test_amount = 430961.9341128137
    responses.add(
        responses.POST,
        SNAPSHOT_SCORES_URL,
        json={
            'jsonrpc': '2.0',
            'result': {'state': 'pending', 'cache': False, 'scores': [
                {BADGER_VOTER_ADDRESS: test_amount}
            ]}, 'id': None
        },
        status=200
    )
    scores = get_scores(
        "aurafinance.eth", "1", TEST_SNAPSHOT_ID,
        [BADGER_VOTER_ADDRESS],
        [{'name': "erc20-votes", 'network': "1", 'params': {
            'symbol': "vlAURA", 'address': "0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC"}}]
    )
    assert scores[BADGER_VOTER_ADDRESS] == test_amount


@responses.activate
def test_get_scores_error():
    responses.add(
        responses.POST,
        SNAPSHOT_SCORES_URL,
        json={},
        status=500
    )
    assert get_scores(
        "aurafinance.eth", "1", TEST_SNAPSHOT_ID,
        [BADGER_VOTER_ADDRESS],
        [{'name': "erc20-votes", 'network': "1", 'params': {
            'symbol': "vlAURA", 'address': "0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC"}}]
    ) is None
