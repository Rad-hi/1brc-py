
def str2f(s: str) -> float:
    endline: bool = s[-1] == '\n'
    is_neg: bool = s[0] == '-'
    sign: int = -10 * is_neg + 10 * (not is_neg)
    sign_offset: int = 1 * is_neg

    res = int(f'{s[sign_offset:-2 - endline]}{s[-1 - endline]}') / sign
    return res
