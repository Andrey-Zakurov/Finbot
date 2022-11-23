# Module for works database
import sqlite3
from random import randrange


# connection DataBase
try:
    database = sqlite3.connect('data.db')
    cursor = database.cursor()
except:
    print("No connection base!!!")



# add testing date from database
def create_test_date():

    for _ in range(100):
        cursor.execute("INSERT INTO income (date, income_sum, descript) VALUES ('21.11.2022 22:50', ?, 'test income')", (randrange(500,2000),))
        database.commit()
        cursor.execute("INSERT INTO expenses (date, expense_sum, descript) VALUES ('21.11.2022 22:50', ?,'test expense')", (randrange(10,2000),))
        database.commit()
    print("testing date add to Database")



# write in the base
def write_to_db(data):

    try:
        cursor.execute("INSERT INTO transactions VALUES(?, ?, ?, ?)", data)
        database.commit()
    except:
        return False
    finally:
        return True


# 10 last payments
def get_list_expens():

    cursor.execute("SELECT date_tr, descript, sum FROM transactions WHERE type = '-' LIMIT 10")
    answer = cursor.fetchall()
    ret = [" | ".join(list(row)) for row in answer]
    return '\n'.join(ret)


# 10 last line of income
def get_list_incom():

    cursor.execute("SELECT date_tr, descript, sum FROM transactions WHERE type = '+' LIMIT 10")
    answer = cursor.fetchall()
    ret = [" | ".join(list(row)) for row in answer]
    return '\n'.join(ret)


# calculation_balance
def get_balance():

    # Test variant!!!!!!!!!!!!!!
    cursor.execute("SELECT SUM(t1.income_sum)-SUM(t2.expense_sum) FROM income AS t1 JOIN expenses AS t2")
    ret = cursor.fetchone()
    print(ret)



if __name__ == "__main__":

    get_balance()
