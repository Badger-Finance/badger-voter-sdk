from typing import Dict
from typing import Optional

from gql import gql

from badger_voter_sdk.collectors.transports import make_gql_client
from badger_voter_sdk.constants import SNAPSHOT_GQL_API_URL

GET_VOTES_Q = ("""
    query Votes {{
      votes (
        first: {first}
        skip: {skip}
        where: {{
          proposal: "{snapshot_id}"
        }}
        orderBy: "created",
        orderDirection: desc
      ) {{
        voter
        choice
      }}
    }}
""")


def get_voters(snapshot_id: str) -> Optional[Dict]:
    """
    Get all voters on given snapshot
    """
    client = make_gql_client(SNAPSHOT_GQL_API_URL)
    limit = 100
    offset = 0
    voters = {}  # type: Dict
    while True:
        result = client.execute(gql(GET_VOTES_Q.format(
            first=limit, skip=offset, snapshot_id=snapshot_id))
        )
        offset += limit
        if not result or not result["votes"]:
            break
        for vote in result['votes']:
            voters[vote['voter']] = vote.get('choice')
    return voters
