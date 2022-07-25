from collections import defaultdict
from decimal import Decimal
from typing import Dict
from typing import Optional

from web3 import Web3


def extract_voting_power_per_pool(
        voters: Dict[str, Dict], scores: Dict
) -> Optional[Dict[str, Decimal]]:
    """
    Extract voting power for each pool, combining two datasets:
    1. voters - has weighed votes per wallet
    2. scores - has data about vlTOKEN voted by wallet

    Returns voting choices calculated in a form {"1": Decimal(123123.04), ...}
    """
    if not voters or not scores:
        return
    # First, map both dataset's wallets to have checksummed addresses
    voters_checksummed = {
        Web3.toChecksumAddress(wallet): choices for wallet, choices in voters.items()
    }
    scores_checksummed = {
        Web3.toChecksumAddress(wallet): totals for wallet, totals in scores.items()
    }
    pool_votes = defaultdict(Decimal)
    for wallet, amount_of_vltoken_voted in scores_checksummed.items():
        voter_choices = voters_checksummed[wallet]
        # All together - represents 100% as it's a vote weight
        all_together = Decimal(sum(voter_choices.values()))
        for pool_choice, weight in voter_choices.items():
            pool_votes[pool_choice] += (
                (Decimal(weight) / all_together) * Decimal(amount_of_vltoken_voted)
            )
    return pool_votes
