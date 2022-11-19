# Module for works database
import sqlite3


# connection DataBase
try:
    database = sqlite3.connect('data.db')
    cursor = database.cursor()
except:
    print("No connection base!!!")


# Create tables for the application
def create_tables():
    database.execute('CREATE TABLE IF NOT EXISTS transactions(type, sum, descript, date_tr)')
    database.execute('CREATE TABLE IF NOT EXISTS types_tr(id, name_type)')
    database.commit()


# write in the base
def write_to_db(data):

    try:
        cursor.execute("INSERT INTO transactions VALUES(?, ?, ?, ?)", data)
        database.commit()
    except:
        return False
    finally:
        return True


def get_list_expens():

    cursor.execute("SELECT date_tr, descript, sum FROM transactions WHERE type = '-'")
    return cursor.fetchall()
