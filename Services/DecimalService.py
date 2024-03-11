def to_decimals(amount, decimals, precision):
    return round((amount / 10 ** decimals), precision)


def from_decimals(amount, decimals, precision):
    return round((amount * 10 ** decimals), precision)
