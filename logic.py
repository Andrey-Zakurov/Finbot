#  Блок с логикой
from db import add_income, add_expenses, get_saldo



def core(message) -> reply message:

    text = message.text.strip()
    ret = []
    if text[0] in '+-':
        ret = [word.strip() for word in text[1:].strip().split(' ', 1)]
        ret.insert(0, text[0])
        ret.append(str(message.date))
        print(ret)
        if len(ret) == 4:
            print(tuple(ret))
            return tuple(ret)


