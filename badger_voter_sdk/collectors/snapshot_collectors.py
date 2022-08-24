import re
from typing import Dict
from typing import Optional

from gql import gql
from web3 import Web3

from badger_voter_sdk.collectors.transports import make_gql_client
from badger_voter_sdk.constants import SNAPSHOT_GQL_API_URL

SNAPSHOT_MIN_AMOUNT_POOLS = 10
SNAPSHOT_STATE_ACTIVE = "active"

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


GET_ACTIVE_PROPOSALS_Q = lambda first, skip, space: gql(f"""
query {{
  proposals (
    first: {first},
    skip: {skip},
    where: {{
      space_in: ["{space}"],
      state: "active"
      network_in: ["1"]
    }},
    orderBy: "created",
    orderDirection: asc
  ) {{
    id
    title
    body
    start
    end
    snapshot
    strategies {{
      name
      network
      params
    }}
    choices
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


def get_gauge_weight_snapshot(web3: Web3, space: str) -> Optional[Dict]:
    """
    Using title re match and some pool heuristics, tries to get current active
    gauge voting proposal. If not found, returns None
    :params:
    - web3: Web3 instance with valid node url
    - space: snapshot voting space, like aurafinance.eth
    """
    client = make_gql_client(SNAPSHOT_GQL_API_URL)
    limit = 100
    offset = 0
    while True:
        result = client.execute(GET_ACTIVE_PROPOSALS_Q(first=limit, skip=offset, space=space))
        offset += limit
        if not result or not result.get("proposals"):
            break
        gauge_proposal = None
        for proposal in result['proposals']:
            if proposal['state'] != SNAPSHOT_STATE_ACTIVE:
                continue
            match = re.match(r"Gauge Weight for Week of .+", proposal['title'])
            number_of_choices = len(proposal['choices'])
            current_timestamp = web3.eth.getBlock(web3.eth.get_block_number())['timestamp']
            # Use heuristics to find out the latest gauge proposal since there is no other way
            # to filter out proposals
            if match and number_of_choices > SNAPSHOT_MIN_AMOUNT_POOLS:
                # Sanity check: proposal should have been started before current date and
                # should end after
                if proposal['end'] > current_timestamp > proposal['start']:
                    gauge_proposal = proposal
                    break
        return gauge_proposal
