# Secrets settings
from enum import Enum

ETHNODEURL_SECRET_ID = "autovoter/web3_ethereum_mainnet_alchemy_api_key"
ETHNODEURL_SECRET_KEY = "NODE_URL"
REGION = "us-west-1"


# API URLs
SNAPSHOT_GQL_API_URL = "https://hub.snapshot.org/graphql"
SNAPSHOT_SCORES_URL = "https://score.snapshot.org/api/scores"
SNAPSHOT_VOTE_API = "https://hub.snapshot.org/api/msg"
COWSWAP_TRADES_URL = "https://api.cow.fi/mainnet/api/v1/trades/"
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

# EOA
BADGER_VOTER_ADDRESS = "0x14F83fF95D4Ec5E8812DDf42DA1232b0ba1015e6"

# misc


class SnapshotType(str, Enum):
    TYPE_1 = "type_1"
    TYPE_2 = "type_2"
