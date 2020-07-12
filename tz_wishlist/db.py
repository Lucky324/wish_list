import sqlite3
import json

import pandas as pd

DB_PATH = ":memory:"

def create_table():
    c.execute("""
        CREATE TABLE wishes
          (
             name   TEXT NOT NULL,
             cost  TEXT NOT NULL,
             link TEXT NOT NULL,
             note TEXT NOT NULL,
             PRIMARY KEY (name)
          ) 
    """)
    conn.commit()

def add_lot(name, cost, link, note):
    add_wish(name, cost, link, note)
    #print_table()

def add_wish(name, cost, link, note):
    c.execute("INSERT INTO wishes VALUES (?, ?, ?, ?)", (name, cost, link, note))
    make_json()
    conn.commit()

def fill_table():
    with open("list.json", "r") as read_file:
        data = json.load(read_file)
    [add_wish(i['name'], i['cost'], i['link'], i['note']) for i in data]

def print_table():
    def print_res(res):
        columns = []
        for col in res:
            columns.append(col)
            print("{:15}".format(col), end="")
        print()
        for i, line in enumerate(res[columns[0]]):
            for c in columns:
                print("{:<15}".format(res[c][i]), end="")
            print()

    print("\nwishes")
    print_res(pd.read_sql_query("SELECT * FROM wishes", conn))

def delete_wish(name):
    c.execute("DELETE FROM wishes WHERE wishes.name = '{}'".format(name))
    #print_table()
    make_json()

def get_wishes():
    x = get_lots(pd.read_sql_query("SELECT * FROM wishes", conn))
    return x

def get_size():
    x = get_lots(pd.read_sql_query("SELECT * FROM wishes", conn))
    return len(x)

def get_lots(res):
    columns = []
    for col in res:
        columns.append(col)
    x = []
    for i, line in enumerate(res[columns[0]]):
        tmp = {
            "name": res['name'][i],
            "cost": res['cost'][i],
            "link": res['link'][i],
            "note": res['note'][i],
        }
        x.append(tmp)
    return x

def make_json():
    x = get_lots(pd.read_sql_query("SELECT * FROM wishes", conn))
    #print(x)
    with open("list.json", "w") as write_file:
        json.dump(x, write_file)

def close_db():
    conn.close()

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
create_table()
fill_table()
#print_table()

