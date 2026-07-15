# 0~9(10개) + A~Z(26개) + a~x(24개) = 총 60진법 지원!
DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwx"

def char_to_value(c):
    if c not in DIGITS:
        raise ValueError(f"잘못된 문자: {c}")
    return DIGITS.index(c)

def value_to_char(v):
    return DIGITS[v]

def str_to_int(num, base):
    value = 0
    abs_base = abs(base)
    # 자리수마다 진법의 거듭제곱을 곱해줌 (음수 진법 자동 지원)
    for i, ch in enumerate(reversed(num)):
        val = char_to_value(ch)
        if val >= abs_base:
            raise ValueError(f"문자 '{ch}'는 절대값 {abs_base}진법에서 사용할 수 없어.")
        value += val * (base ** i)
    return value

def int_to_str(num, base, length=4):
    if num == 0:
        return "0" * length

    s = ""
    abs_base = abs(base)
    while num != 0:
        # 음수 진법 나눗셈의 핵심! 나머지는 항상 '양수'로 나와야 자릿수가 됨
        remainder = num % abs_base
        num = (num - remainder) // base
        s = value_to_char(remainder) + s

    return s.rjust(length, "0")

def run_kaprekar(base, number):
    # 4자리로 맞춤 (대소문자 구분을 위해 upper() 제거)
    number = number.zfill(4)
    
    # 해당 진법에서 올바른 숫자인지 사전 검증
    str_to_int(number, base)

    history = []
    steps = []

    while True:
        # 문자의 '가치'를 기준으로 정렬 (a가 Z보다 큼)
        sorted_chars = sorted(number, key=lambda x: char_to_value(x))
        high = "".join(reversed(sorted_chars))
        low = "".join(sorted_chars)

        big = str_to_int(high, base)
        small = str_to_int(low, base)

        # 음수 진법에서도 동일하게 큰 수에서 작은 수를 뺌
        diff = big - small
        nxt = int_to_str(diff, base, 4)

        steps.append({
            "high": high,
            "low": low,
            "result": nxt
        })

        if nxt == number:
            return {"status": "constant", "constant": nxt, "steps": steps, "count": len(steps)}

        if nxt in history:
            start = history.index(nxt)
            loop = history[start:] + [nxt]
            return {"status": "loop", "loop": loop, "steps": steps, "count": len(steps)}

        history.append(number)
        number = nxt
