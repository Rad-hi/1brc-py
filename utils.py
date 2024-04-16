
def str2f(s: str) -> float:
    endline: bool = s[-1] == '\n'
    is_neg: bool = s[0] == '-'
    sign: int = -10 * is_neg + 10 * (not is_neg)
    sign_offset: int = 1 * is_neg

    res = int(f'{s[sign_offset:-2 - endline]}{s[-1 - endline]}') / sign
    return res

def bytes2int(s: bytes) -> int:
    ORD_0 = 48
    endline: bool = s[-1] == 10  # ord('\n') == 10
    is_neg: bool = s[0] == 45  # ord('-') == 45
    is_double: bool = s[is_neg + 1] != 46  # ord('.') == 46
    sign: int = -1 * is_neg + 1 * (not is_neg)

    res = s[-1 - endline]
    if is_double:
        res += s[is_neg] * 100 + s[is_neg + 1] * 10 - (111 * ORD_0)
    else:
        res += s[is_neg] * 10 - (11 * ORD_0)

    return sign * res
