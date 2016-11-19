import sqlite3
import numpy as np


def get_data(stock_name='YHOO'):
    conn = sqlite3.connect('stockHistory.db')
    cursor = conn.cursor()
    stock_name = tuple([stock_name])
    N = 10
    # find the max date of the records in DB
    cursor.execute('SELECT TradePrice FROM TrueTimeValue '
                   'WHERE Symbol =? ORDER BY TadeTime DESC '
                   'LIMIT 10', stock_name)
    dataset = cursor.fetchall()
    print dataset
    dataset.reverse()
    Y = np.array(dataset).reshape(N, 1)
    # print Y

    conn.commit()
    cursor.close()
    conn.close()
    return Y


if __name__=='__main__':
    print get_data('YHOO')