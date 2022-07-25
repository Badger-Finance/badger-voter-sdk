from typing import Dict
from typing import List
from typing import Optional

import requests

from badger_voter_sdk.constants import SNAPSHOT_SCORES_URL
from badger_voter_sdk.rich_logger import logger


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
