#!/usr/bin/python
# -*- coding: utf-8 -*-

import putFunc

#this script inserts things into the mysql database that is installed on this system

#variables that are inserted into the database
#quotedt parameters 
stringDatetime = "2001-01-18 01:15:08"
#option static parameter s
underlyingSymbol = "TEST"
stringExpiration = "2002-01-18 01:15:08"
strike = 300
option_type = 'C'
#dynamic parameters 
root = "TEST"
openPrice = 10.0
high = 15.0
low = 8.0
close = 9.0
trade_volume = 100000
bid_size = trade_volume/2
bid = 10.0
ask_size = trade_volume/2
ask = 11.0
implied_underlying_price = 100.0
implied_volitility = 0.25
delta = 0.50
gamma = 0.1
theta = 0.21
vega = 0.25
rho = 0.01
#underlying parameters
underlying_bid = 100
underlying_ask = 100
active_underlying_price = 100





import MySQLdb as mdb

con = mdb.connect('localhost','pythonuser','snake','tradingData');

with con:

    cur = con.cursor()

    #quotedt insertion event
    cur.execute("INSERT INTO quotedt( dt ) VALUES( %s )",(stringDatetime,))
    #store id in variable
    cur.execute("SELECT LAST_INSERT_ID() INTO @qdt_id")

    #opStaticPs insertion 
    cur.execute("INSERT INTO opStaticPs(underlyingSymbol,expiration,strike,op_type) "\
                "VALUES(%s,%s,%s,%s)",(underlyingSymbol,stringExpiration,strike,option_type,))
    #store opStatic id 
    cur.execute("SELECT LAST_INSERT_ID() INTO @static_id");
    #insert into option dynamic 
    cur.execute("INSERT INTO opDynamicPs(root,open,high,low,close,trade_volume," \
                "bid_size,bid,ask_size,ask,implied_underlying_price,implied_volitility,"\
                "delta,gamma,theta,vega,rho,opStaticPs_id,quotedt_id)"
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"\
                "%s,%s,@static_id,@qdt_id)",(root,openPrice,high,low,close,trade_volume,
                                           bid_size,bid,ask_size,ask,implied_underlying_price,
                                           implied_volitility,delta,gamma,theta,vega,rho))
    
    #insert into underlyings 
    cur.execute("INSERT INTO underlyings(underlying_bid,underlying_ask,active_underlying_price,quotedt_id)"\
                "VALUES(%s,%s,%s,@qdt_id)",(underlying_bid,underlying_ask,active_underlying_price))
    #select data and print
    #cur.execute("SELECT id FROM quotedt WHERE dt = '2001-01-18 01:15:08'");
    #rows = cur.fetchall();
   # if not rows:
    #    print "false"
    #for row in rows:
      #  print row;

    print putFunc.put_dt(cur,'2003-01-18 01:18:14')
    
