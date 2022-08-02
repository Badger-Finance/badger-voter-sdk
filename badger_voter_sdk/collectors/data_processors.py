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
    if not all([voters, scores]):
        return
    # First, map both dataset's wallets to have checksummed addresses
    voters_checksummed = {}
    for wallet, choices in voters.items():
        voters_checksummed[Web3.toChecksumAddress(wallet)] = {
            choice: Decimal(value) for choice, value in choices.items()
        }
    scores_checksummed = {
        Web3.toChecksumAddress(wallet): Decimal(totals) for wallet, totals in scores.items()
    }
    pool_votes = defaultdict(Decimal)
    for wallet, amount_of_vltoken_voted in scores_checksummed.items():
        voter_choices = voters_checksummed[wallet]
        # All together - represents 100% as it's a vote weight
        all_together = sum(voter_choices.values())
        if all_together == Decimal(0):
            continue
        for pool_choice, weight in voter_choices.items():
            pool_votes[pool_choice] += (
                (weight / all_together) * amount_of_vltoken_voted
            )
    return pool_votes


def extract_voting_power_per_eoa(
        target_wallet: str, voters: Dict[str, Dict], scores: Dict
) -> Optional[Dict[str, Decimal]]:
    """
    Extract voting power by wallet, combining two datasets:
        1. voters - has weighed votes per wallet
        2. scores - has data about vlTOKEN voted by wallet

    Returns voting choices for wallet calculated in a form {"1": Decimal(123123.04), ...}
    """
    if not all([target_wallet, voters, scores]):
        return
    # First, map both dataset's wallets to have checksummed addresses
    voters_checksummed = {}
    for wallet, choices in voters.items():
        voters_checksummed[Web3.toChecksumAddress(wallet)] = {
            choice: Decimal(value) for choice, value in choices.items()
        }
    scores_checksummed = {
        Web3.toChecksumAddress(wallet): Decimal(totals) for wallet, totals in scores.items()
    }
    eoa_checksummed = Web3.toChecksumAddress(target_wallet)
    amount_of_vltoken_voted = scores_checksummed.get(eoa_checksummed)
    voter_choices = voters_checksummed.get(eoa_checksummed)
    if not amount_of_vltoken_voted or not voters:
        return
    # All together - represents 100% as it's a vote weight
    all_together = sum(voter_choices.values())
    if all_together == Decimal(0):
        return
    return {
        pool_choice: (weight / all_together) * amount_of_vltoken_voted
        for pool_choice, weight in voter_choices.items()
    }
