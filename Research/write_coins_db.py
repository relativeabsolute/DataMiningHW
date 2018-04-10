import coins
import sqlite3

def write():
    conn = sqlite3.connect('coins.db')

    c = conn.cursor()

    for coin in coins.coin_ids:
        c.execute('insert into coins (ccc_coin_id, name, symbol) values (?,?,?)',
                (coin['id'], coin['name'], coin['symbol']))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    write()
