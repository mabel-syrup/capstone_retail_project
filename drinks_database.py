import sqlite3
from marshal import dumps as pack, loads as unpack

sqlite_file = "drinks.sqlite"
hot = 'hot_drinks_table'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


def make_db_if_deleted():
    c.execute("CREATE TABLE hot_drinks_table (Name TEXT PRIMARY KEY, Abbreviation TEXT, Short BLOB, Tall BLOB, Grande BLOB, Venti BLOB)")
    conn.commit()


def close():
    conn.close()


def dpack(data):
    data_bytes = pack(data)
    #print('Type of data_bytes is {}'.format(type(data_bytes)))
    out_str = str(pack(data)).replace("'", "''")
    #print(out_str)
    return out_str



def add_recipe(name, abbreviation, steps):
    try:
        steps_short = pack(steps[0])
        steps_tall = pack(steps[1])
        steps_grande = pack(steps[2])
        steps_venti = pack(steps[3])
        #print("Venti: {}: {}".format(type(steps_venti),str(steps_venti)))
    except KeyError:
        print("{} steps not given in correct format!  Skipping...".format(name))
        return
    #c.execute("INSERT INTO {} (Name) VALUES ('Latte')".format(hot))
    c.execute("INSERT OR IGNORE INTO {} (Name,Abbreviation,Short,Tall,Grande,Venti) VALUES ('{}','{}',?,?,?,?)"
              .format(hot, name, abbreviation),(steps_short, steps_tall, steps_grande, steps_venti))
    conn.commit()

def get_drink_recipe(name,size):
    c.execute("SELECT {} FROM {} WHERE Name='{}'".format(size,hot,name))
    steps_raw = c.fetchone()[0]
    try:
        steps = unpack(steps_raw)
        #print("Steps: {}".format(type(steps)))
        return steps
    except Exception:
        print("Unable to unpack steps!")
        return ''

def get_drink_abbreviation(name):
    c.execute("SELECT Abbreviation FROM {} WHERE Name='{}'".format(hot,name))
    abb = c.fetchone()[0]
    return abb

def get_drink_names():
    c.execute("SELECT (Name) FROM {}".format(hot))
    all_names = c.fetchall()
    return all_names