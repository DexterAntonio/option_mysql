#!/user/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time 

yaxis = "bid" 
con = mdb.connect('localhost','pythonuser','snake','tradingData');

with con:
    cur = con.cursor()
    cur.execute("SELECT quotedt.dt, opDynamicPs.bid FROM opDynamicPs INNER JOIN quotedt ON opDynamicPs.quotedt_id = quotedt.id WHERE opStaticPs_id=3033")
    dataTuple = cur.fetchall()

    
dates = [] # np.zeros(len(dataTuple),dtype='datetime64[s]')
values = np.zeros(len(dataTuple))

for i in range(0,len(dataTuple)):
    tmp = dataTuple[i]
    #dates[i] = tmp[0]
    dates.append(tmp[0])
    values[i] = tmp[1]

plt.plot_date(dates,values,'-')
plt.xlabel("date")
plt.ylabel(yaxis)

plt.show() 

#also fix mysql database 

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM expiration")
    rows = cur.fetchall() 
    for row in rows: 
        ids = row[0]
        dt = row[1] 
        cur.execute("SELECT id FROM opStaticPs WHERE opStaticPs.expiration = %s",(dt,))
        static_ids = cur.fetchall()
        for static_id in static_ids:
            cur.execute("UPDATE opStaticPs SET expiration_id = %s WHERE id = %s",(ids,static_id))



