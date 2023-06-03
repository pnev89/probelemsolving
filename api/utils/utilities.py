
import json
from typing import Dict
import pandas as pd

# Parsing data to deliver
def parse_to_json(data_: pd.DataFrame) -> Dict:
    """Parse data into json.

    Parameters
    ----------
    data_ : pd.DataFrame
        Data to be parsed

    Returns
    -------
    Dict
        Data parsed
    """
    res = data_.to_json(orient="table")
    parsed = json.loads(res)
    return parsed["data"]