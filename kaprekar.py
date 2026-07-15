DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def char_to_value(c):
    return DIGITS.index(c.upper())

def value_to_char(v):
    return DIGITS[v]

def str_to_int(num, base):
    value = 0
    for ch in num:
        value = value * base + char_to_value(ch)
    return value

def int_to_str(num, base, length=4):
    if num == 0:
        return "0".rjust(length, "0")

    s = ""
    while num > 0:
        s = value_to_char(num % base) + s
        num //= base

    return s.rjust(length, "0")


def run_kaprekar(base, number):

    number = number.upper()

    history = []
    steps = []

    while True:

        high = "".join(sorted(number, reverse=True))
        low = "".join(sorted(number))

        big = str_to_int(high, base)
        small = str_to_int(low, base)

        diff = big - small

        nxt = int_to_str(diff, base, len(number))

        steps.append({
            "high": high,
            "low": low,
            "result": nxt
        })

        if nxt == number:
            return {
                "status": "constant",
                "constant": nxt,
                "steps": steps
            }

        if nxt in history:

            start = history.index(nxt)

            return {
                "status": "loop",
                "loop": history[start:] + [nxt],
                "steps": steps
            }

        history.append(number)
        number = nxt
