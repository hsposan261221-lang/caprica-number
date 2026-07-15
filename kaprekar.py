def to_decimal(num,base):

    return int(num,base)


def from_decimal(num,base,length=4):

    chars="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    ans=""

    while num:

        ans=chars[num%base]+ans
        num//=base

    ans=ans.rjust(length,"0")

    return ans


def run_kaprekar(base,number):

    history=[]

    steps=[]

    while True:

        high="".join(sorted(number,reverse=True))

        low="".join(sorted(number))

        diff=to_decimal(high,base)-to_decimal(low,base)

        nxt=from_decimal(diff,base,len(number))

        steps.append(
            f"{high} - {low} = {nxt}"
        )

        if nxt==number:

            return{
                "type":"constant",
                "value":nxt,
                "steps":steps
            }

        if nxt in history:

            return{
                "type":"loop",
                "value":nxt,
                "steps":steps
            }

        history.append(number)

        number=nxt
