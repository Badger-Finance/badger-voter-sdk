from decimal import Decimal
from typing import Dict
from typing import List
from typing import Optional

import requests

from badger_voter_sdk.constants import BINANCE_KLINES_URL
from badger_voter_sdk.constants import COWSWAP_TRADES_URL
from badger_voter_sdk.constants import SNAPSHOT_SCORES_URL
from badger_voter_sdk.json_logger import logger

MINUTE_INTERVAL = 60  # in seconds
BINANCE_TIMESTAMP_MULTIPLIER = 1000


def get_scores(
        space: str, network: str, snapshot_id: str, addresses: List[str], strategies: List[Dict]
) -> Optional[Dict]:
    """
    Fetch amount of votes per wallet in 'addresses' param. This is needed to calculate amount
    of votes per pool
    """
    response = requests.post(SNAPSHOT_SCORES_URL, json={'params': {
        'space': space, 'network': network,
        'snapshot': snapshot_id,
        'addresses': addresses,
        'strategies': strategies
    }})
    if not response.ok:
        logger.error(f"Cannot fetch scores for snapshot: {snapshot_id}")
        return None
    return response.json()['result']['scores'][0]


def get_cowswap_trades_by_order(orders: List[str]) -> List[Dict]:
    """
    Helper function to return multiple orders from cowswap
    """
    fetched_orders = []
    for order in orders:
        order_response = requests.get(COWSWAP_TRADES_URL, params={'orderUid': order})
        if not order_response.ok:
            logger.error(f"Cannot fetch order {order} from Cowswap")
            continue
        fetched_orders.append(order_response.json())
    return fetched_orders


def fetch_binance_price_for_given_dt(
        deal_closed_timestamp: int, token_pair: str) -> Decimal:
    """
    Fetch Token prices from Binance API
    """
    start_time = int(deal_closed_timestamp) - MINUTE_INTERVAL  # convert datetime to timestamp
    end_time = deal_closed_timestamp
    params = {
        'symbol': token_pair,
        'interval': "1m",
        'startTime': start_time * BINANCE_TIMESTAMP_MULTIPLIER,
        'endTime': end_time * BINANCE_TIMESTAMP_MULTIPLIER
    }
    response = requests.get(BINANCE_KLINES_URL, params)
    if response.ok:
        # Record first usd price from interval. 4th element is `close` price for interval
        return Decimal(response.json()[0][4])
    else:
        return Decimal(0)
