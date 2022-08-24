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


GET_SINGLE_PROPOSAL_Q = lambda snapshot_id: gql(f"""
query {{
  proposals (
    first: 1,
    skip: 0,
    where: {{
      network_in: ["1"]
      id: "{snapshot_id}"
    }},
    orderBy: "created",
    orderDirection: desc
  ) {{
    id
    title
    body
    start
    end
    snapshot
    choices
    strategies {{
      name
      network
      params
    }}
    network
    state
    author
    space {{
      id
      name
    }}
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


def get_snapshot_by_id(snapshot_id: str) -> Optional[Dict]:
    """
    Get single snapshot by id
    """
    client = make_gql_client(SNAPSHOT_GQL_API_URL)
    result = client.execute(GET_SINGLE_PROPOSAL_Q(snapshot_id))
    if not result or not result.get("proposals"):
        return
    target_snapshot = None
    for proposal in result['proposals']:
        if proposal['id'] == snapshot_id:
            target_snapshot = proposal
    return target_snapshot
