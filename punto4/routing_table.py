# routing_table.py
# Single source of truth for ABA routing numbers and checksum validation

ROUTING_TABLE = {
    ("bank of america", "texas"):           "111000025",
    ("bank of america", "california"):      "121000358",
    ("bank of america", "new york"):        "021200339",
    ("jpmorgan chase", "new york"):         "021000021",
    ("jpmorgan chase", "texas"):            "111000614",
    ("jpmorgan chase", "california"):       "322271627",
    ("wells fargo", "california"):          "121000248",
    ("wells fargo", "texas"):               "111900659",
    ("wells fargo", "new york"):            "026012881",
    ("citibank", "new york"):               "021000089",
    ("citibank", "california"):             "322271724",
    ("pnc bank", "ohio"):                   "043000096",
    ("pnc bank", "pennsylvania"):           "031100089",
    ("capital one", "virginia"):            "051405515",
    ("capital one", "new york"):            "026013673",
    ("td bank", "new jersey"):              "031201360",
    ("td bank", "new york"):                "026013673",
    ("santander bank", "massachusetts"):    "011075150",
    ("santander bank", "new york"):         "021407912",
    ("u.s. bank", "minnesota"):             "091000022",
    ("u.s. bank", "california"):            "122235821",
    ("regions bank", "alabama"):            "062000019",
    ("regions bank", "florida"):            "063104668",
}


def lookup_routing(bank: str, state: str) -> str | None:
    """
    Returns routing number for a given bank and state.
    Normalizes input to lowercase before lookup.
    Returns None if combination is not found.
    """
    key = (bank.lower().strip(), state.lower().strip())
    return ROUTING_TABLE.get(key, None)


def validate_checksum(routing: str) -> bool:
    """
    Validates ABA routing number using Nacha checksum formula:
    3(d1+d4+d7) + 7(d2+d5+d8) + (d3+d6+d9) must be divisible by 10.
    """
    if len(routing) != 9 or not routing.isdigit():
        return False
    d = [int(c) for c in routing]
    checksum = (
        3 * (d[0] + d[3] + d[6]) +
        7 * (d[1] + d[4] + d[7]) +
        1 * (d[2] + d[5] + d[8])
    )
    return checksum % 10 == 0
