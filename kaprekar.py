DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def char_to_value(c):
    c = c.upper()
    if c not in DIGITS:
        raise ValueError(f"잘못된 문자: {c}")
    return DIGITS.index(c)

def value_to_char(v):
    return DIGITS[v]

def str_to_int(num, base):
    value = 0
    for ch in num:
        if char_to_value(ch) >= base:
            raise ValueError(f"{ch}는 {base}진법에서 사용할 수 없습니다.")
        value = value * base + char_to_value(ch)
    return value

def int_to_str(num, base, length=4):
    if num == 0:
        return "0" * length

    s = ""
    while num > 0:
        s = value_to_char(num % base) + s
        num //= base

    return s.rjust(length, "0")


def run_kaprekar(base, number):

    number = number.upper().zfill(4)

    history = []
    steps = []

    while True:

        high = "".join(sorted(number, reverse=True))
        low = "".join(sorted(number))

        big = str_to_int(high, base)
        small = str_to_int(low, base)

        diff = big - small

        nxt = int_to_str(diff, base, 4)

        steps.append({
            "high": high,
            "low": low,
            "result": nxt
        })

        if nxt == number:
            return {
                "status": "constant",
                "constant": nxt,
                "steps": steps,
                "count": len(steps)
            }

        if nxt in history:
            start = history.index(nxt)
            loop = history[start:] + [nxt]
            return {
                "status": "loop",
                "loop": loop,
                "steps": steps,
                "count": len(steps)
            }

        history.append(number)
        number = nxt
