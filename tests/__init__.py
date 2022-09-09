import json
import os
from typing import Dict
from typing import List
from typing import Union


def parse_fixture_json(file_name: str) -> Union[Dict, List[Dict]]:
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test_data",
        file_name
    )
    with open(path) as file:
        data = json.load(file)
    return data
