# Badger SDK for autovoters

This is the library for shared code that is used in autovoters, such as cvx autovoter and aura autovoter

| Build  | Coverage | PYPI | 
| ------------- | ------------- | ------------- |
| [![Tests](https://github.com/Badger-Finance/badger-voter-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/Badger-Finance/badger-voter-sdk/actions/workflows/test.yml) | [![codecov](https://codecov.io/gh/Badger-Finance/badger-voter-sdk/branch/main/graph/badge.svg?token=UYLO67O4Q9)](https://codecov.io/gh/Badger-Finance/badger-voter-sdk)  | [![PyPI version](https://badge.fury.io/py/badger-voter-sdk.svg)](https://badge.fury.io/py/badger-voter-sdk) |


## List of functional modules:

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