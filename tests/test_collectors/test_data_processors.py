from decimal import Decimal

import pytest

from badger_voter_sdk.collectors.data_processors import extract_voting_power_per_pool
from badger_voter_sdk.constants import BADGER_VOTER_ADDRESS
from tests.test_data.datasets import SCORES_DATASET
from tests.test_data.datasets import VOTERS_DATASET


def test_extract_voting_power_per_pool_happy():
    pools_totals = extract_voting_power_per_pool(VOTERS_DATASET, SCORES_DATASET)
    assert pools_totals == {'2': Decimal('754367.6264015021129303180640'),
                            '10': Decimal('388949.0270256447689109176822'),
                            '38': Decimal('206410.0705127691805272738961'),
                            '46': Decimal('74299.26534898661555583418960'),
                            '72': Decimal('51554.88265129792529654596594'),
                            '8': Decimal('16349.58836052620150525171994'),
                            '49': Decimal('35125.74760370352206157078807'),
                            '64': Decimal('16300.65735959238372743129731'),
                            '65': Decimal('16300.65735959238372743129731'),
                            '83': Decimal('215932.2064030202473913097701'),
                            '3': Decimal('462240.1750155773838228198063'),
                            '34': Decimal('111605.1532668299708437463721'),
                            '1': Decimal('136975.8414888792239253234584'),
                            '17': Decimal('88931.34068345901239332423277'),
                            '43': Decimal('93724.85276205035245507676238'),
                            '37': Decimal('37860.19496799834065083303132'),
                            '45': Decimal('84555.94628210251970954493929'),
                            '47': Decimal('63933.91038278411053141780939'),
                            '4': Decimal('1755.809364619091862635968936'),
                            '5': Decimal('1265.550168131053698772348070'),
                            '7': Decimal('31.51672954786348057609757234'),
                            '29': Decimal('31.51672954786348057609757234'),
                            '30': Decimal('33281.22535584166430627167048'),
                            '35': Decimal('16691.33290514745012858257824'),
                            '42': Decimal('962.0683970465643710667791311'),
                            '27': Decimal('19.89541499151663117572752526'),
                            '31': Decimal('40.57618178129438035739440238'),
                            '80': Decimal('7232.114174461107637625900680')}


def test_extract_voting_power_per_pool_precalc_equal():
    equal_part = 100.00 / 3
    total_vl_tokens = 430961.9341128137
    expected = Decimal(equal_part / 100 * total_vl_tokens)
    pools_totals = extract_voting_power_per_pool(
        {
            BADGER_VOTER_ADDRESS: {'1': equal_part, '2': equal_part, '3': equal_part}
        },
        {
            BADGER_VOTER_ADDRESS: 430961.9341128137
        })
    for _, votes in pools_totals.items():
        assert votes == pytest.approx(expected)


def test_extract_voting_power_per_pool_empty():
    assert not extract_voting_power_per_pool(VOTERS_DATASET, {})
