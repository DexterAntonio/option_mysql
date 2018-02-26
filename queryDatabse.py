#!/user/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time 

yaxis = "delta" 
con = mdb.connect('localhost','pythonuser','snake','tradingData');

with con:
    cur = con.cursor()
    cur.execute("SELECT quotedt.dt, opDynamicPs.delta FROM opDynamicPs INNER JOIN quotedt ON opDynamicPs.quotedt_id = quotedt.id WHERE opStaticPs_id=3036")
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
