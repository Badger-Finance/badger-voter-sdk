from decimal import Decimal

import responses

from badger_voter_sdk.collectors.api_collectors import fetch_binance_price_for_given_dt
from badger_voter_sdk.collectors.api_collectors import get_cowswap_trades_by_order
from badger_voter_sdk.collectors.api_collectors import get_scores
from badger_voter_sdk.constants import BADGER_VOTER_ADDRESS
from badger_voter_sdk.constants import BINANCE_KLINES_URL
from badger_voter_sdk.constants import COWSWAP_TRADES_URL
from badger_voter_sdk.constants import SNAPSHOT_SCORES_URL
from tests import parse_fixture_json

TEST_SNAPSHOT_ID = "0x9a21d743bbdf54f2505f022564686c0431d5e95771318f2b67c807960ae4bd8d"
MOCK_ORDER_UID = "0xaa77ca57aa9449087bbd6fa258078825da99349bc746a9a6e61a816ae5a73a1a6f76" \
                 "c6a1059093e21d8b1c13c4e20d8335e2909f62713f32"


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


@responses.activate
def test_fetch_cowswap_orders_happy():
    order = parse_fixture_json("cowswap_order.json")
    responses.add(
        responses.GET,
        f"{COWSWAP_TRADES_URL}?orderUid={MOCK_ORDER_UID}",
        json=order, status=200
    )
    orders = get_cowswap_trades_by_order([MOCK_ORDER_UID])
    assert orders == [order]


@responses.activate
def test_fetch_cowswap_orders_unhappy():
    responses.add(
        responses.GET,
        f"{COWSWAP_TRADES_URL}?orderUid={MOCK_ORDER_UID}",
        json={}, status=400
    )
    orders = get_cowswap_trades_by_order([MOCK_ORDER_UID])
    assert orders == []


@responses.activate
def test_fetch_binance_prices_happy_cvx():
    responses.add(
        responses.GET,
        BINANCE_KLINES_URL,
        json=[
            [1651585260000, '22.59000000', '22.60000000', '22.57000000', '22.57000000',
             '64.63700000', 1651585319999, '1459.50512000', 6, '1.45600000', '32.90560000', '0']
        ], status=200
    )
    result = fetch_binance_price_for_given_dt(
        1651585260000,
        token_pair='CVXUSDT'
    )
    assert result == Decimal('22.57000000')


@responses.activate
def test_fetch_binance_prices_happy_badger():
    responses.add(
        responses.GET,
        BINANCE_KLINES_URL,
        json=[
            [1651585260000, '7.59000000', '7.60000000', '7.57000000', '7.57000000',
             '64.63700000', 1651585319999, '1459.50512000', 6, '1.45600000', '32.90560000', '0']
        ], status=200
    )
    result = fetch_binance_price_for_given_dt(
        1651585260000,
        token_pair='BADGERUSDT'
    )
    assert result == Decimal('7.57000000')


@responses.activate
def test_fetch_binance_prices_unhappy():
    responses.add(
        responses.GET,
        BINANCE_KLINES_URL,
        json=[], status=400
    )
    assert not fetch_binance_price_for_given_dt(1651585260000, 'CVXUSDT')
