# Badger SDK for autovoters

This is the library for shared code that is used in autovoters, such as cvx autovoter and aura autovoter

| Build  | Coverage | PYPI | 
| ------------- | ------------- | ------------- |
| [![Tests](https://github.com/Badger-Finance/badger-voter-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Badger-Finance/badger-voter-sdk/actions/workflows/test.yml) | [![codecov](https://codecov.io/gh/Badger-Finance/badger-voter-sdk/branch/main/graph/badge.svg?token=UYLO67O4Q9)](https://codecov.io/gh/Badger-Finance/badger-voter-sdk)  | [![PyPI version](https://badge.fury.io/py/badger-voter-sdk.svg)](https://badge.fury.io/py/badger-voter-sdk) |


## List of functional modules:

## Utilities

--- 

### Get web3 instance

```python
import os
from badger_voter_sdk.web3 import get_web3

web3 = get_web3(os.getenv("ETHNODEURL"))
```
Or web3 will be created from default secrets in `constants.py`


### AWS get secret
Getting secret from AWS by id and key

```python
from badger_voter_sdk.aws import get_secret

secret = get_secret(secret_id="SecretId", secret_key="SecretKey")
```


### Rich logger
Preconfigured rich logger to be shared across voting bots projects

```python
from badger_voter_sdk.rich_logger import logger

logger.info()
```

## Snapshot and data collectors

### Get all voters for snapshot

```python
from badger_voter_sdk.collectors.snapshot_collectors import get_voters

voters = get_voters(snapshot_id="some_snapshot_id")
```

### Get vlTOKEN amounts per wallet voted for given snapshot round

```python
from badger_voter_sdk.collectors.api_collectors import get_scores

scores = get_scores(
    "aurafinance.eth", "1", "<SNAPSHOT_ID>",
    ["<ADDRESS1>"],
    [{'name': "erc20-votes", 'network': "1", 'params': {
        'symbol': "<vlTOKEN>", 'address': "<STRATEGY_ADDR>"}}]
)
```

### Get voting choices with voting power
You need to combine two previous functions outputs:

```python
from badger_voter_sdk.collectors.data_processors import extract_voting_power_per_pool

choices_with_votes = extract_voting_power_per_pool(voters={"<wallet>": {"1": 123}}, scores={"<wallet>": 123333.1})
```
