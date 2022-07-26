from copy import deepcopy
from decimal import Decimal

import pytest

from badger_voter_sdk.collectors.data_processors import extract_voting_power_per_eoa
from badger_voter_sdk.collectors.data_processors import extract_voting_power_per_pool
from badger_voter_sdk.constants import BADGER_VOTER_ADDRESS
from tests.test_data.datasets import SCORES_DATASET
from tests.test_data.datasets import VOTERS_DATASET


def test_extract_voting_power_per_pool_happy():
    pools_totals = extract_voting_power_per_pool(VOTERS_DATASET, SCORES_DATASET)
    assert pools_totals == {'1': Decimal('136975.8414888792239253234584'),
                            '10': Decimal('388949.0270256447871415391373'),
                            '17': Decimal('88931.34068345901239332423277'),
                            '2': Decimal('754367.6264015021129303180640'),
                            '27': Decimal('19.89541499151663117572752526'),
                            '29': Decimal('31.51672954786348057609757234'),
                            '3': Decimal('462240.1750155773838228198063'),
                            '30': Decimal('33281.22535584166430627167048'),
                            '31': Decimal('40.57618178129438035739440238'),
                            '34': Decimal('111605.1532668299708437463721'),
                            '35': Decimal('16691.33290514745012858257824'),
                            '37': Decimal('37860.19496799834065083303132'),
                            '38': Decimal('206410.0705127692021017835899'),
                            '4': Decimal('1755.809364619091862635968936'),
                            '42': Decimal('962.0683970465643710667791311'),
                            '43': Decimal('93724.85276205035245507676238'),
                            '45': Decimal('84555.94628210251970954493929'),
                            '46': Decimal('74299.26534898662477832082219'),
                            '47': Decimal('63933.91038278411053141780939'),
                            '49': Decimal('35125.74760370352206157078807'),
                            '5': Decimal('1265.550168131053698772348070'),
                            '64': Decimal('16300.65735959238372743129731'),
                            '65': Decimal('16300.65735959238372743129731'),
                            '7': Decimal('31.51672954786348057609757234'),
                            '72': Decimal('51554.88265129792985688072733'),
                            '8': Decimal('16349.58836052620150525171994'),
                            '80': Decimal('7232.114174461107637625900680'),
                            '83': Decimal('215932.2064030202473913097701')}


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


def test_extract_voting_power_per_eoa_happy():
    # Badger delegate EOA
    target_eoa = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"
    eoa_totals = extract_voting_power_per_eoa(
        target_eoa, VOTERS_DATASET, SCORES_DATASET
    )
    assert eoa_totals == {'10': Decimal('146613.2499851792224176974254'),
                          '38': Decimal('173505.2746738187730864708968'),
                          '46': Decimal('74168.54886081523547733346492'),
                          '72': Decimal('36674.86059300044200065448964')}
    assert sum(eoa_totals.values()) == pytest.approx(Decimal(SCORES_DATASET[target_eoa]))


def test_extract_voting_power_per_eoa_no_scores():
    target_eoa = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"
    scores = deepcopy(SCORES_DATASET)
    scores.pop(target_eoa)
    assert not extract_voting_power_per_eoa(
        target_eoa, VOTERS_DATASET, scores
    )


def test_extract_voting_power_per_eoa_no_voters_choices():
    target_eoa = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"
    voters = deepcopy(VOTERS_DATASET)
    voters[target_eoa] = {'1': 0.0}
    assert not extract_voting_power_per_eoa(
        target_eoa, voters, SCORES_DATASET
    )


def test_extract_voting_power_per_eoa_empty():
    target_eoa = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"
    assert not extract_voting_power_per_eoa(
        target_eoa, VOTERS_DATASET, {}
    )
