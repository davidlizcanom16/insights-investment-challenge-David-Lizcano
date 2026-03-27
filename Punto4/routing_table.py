# routing_table.py
# Single source of truth for ABA routing numbers and checksum validation

ROUTING_TABLE = {
    # Bank of America
    ("bank of america", "texas"):           "111000025",
    ("bank of america", "california"):      "121000358",
    ("bank of america", "new york"):        "021200339",

    # JPMorgan Chase
    ("jpmorgan chase", "new york"):         "021000021",
    ("jpmorgan chase", "texas"):            "111000614",
    ("jpmorgan chase", "california"):       "322271627",

    # Wells Fargo
    ("wells fargo", "california"):          "121000248",
    ("wells fargo", "texas"):               "111900659",
    ("wells fargo", "new york"):            "026012881",

    # Citibank
    ("citibank", "new york"):               "021000089",
    ("citibank", "california"):             "322271724",
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
