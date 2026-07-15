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
        val = char_to_value(ch)
        if val >= base:
            raise ValueError(f"문자 '{ch}'는 {base}진법에서 사용할 수 없어.")
        value = value * base + val
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
    # 입력받은 숫자를 무조건 대문자 및 4자리로 맞춤 (예: "24" -> "0024")
    number = number.upper().zfill(4)
    
    # 해당 진법에서 쓸 수 없는 숫자가 있는지 미리 검사
    str_to_int(number, base)

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

        # 귀착수(상수) 발견
        if nxt == number:
            return {
                "status": "constant",
                "constant": nxt,
                "steps": steps,
                "count": len(steps)
            }

        # 루프 발견
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
