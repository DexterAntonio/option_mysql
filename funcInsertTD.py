#!/usr/bin/python
# -*- coding: utf-8 -*-

import putFunc
import MySQLdb as mdb


#variables that are inserted into the database
#quotedt parameters 
sDateTime = "2001-01-18 01:15:08"
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


con = mdb.connect('localhost','pythonuser','snake','tradingData');

with con:
    qdt_id = 0
    opStatic_id = 0
    
    cur = con.cursor()

    #quotedt insertion event
    qdt_id = putFunc.put_dt(cur,sDateTime) 

    #opStaticPs insertion
    opStatic_id = putFunc.put_opStatic(cur, underlyingSymbol,stringExpiration,strike,option_type)
    #insert into option dynamic 
    putFunc.put_opDynamic(cur,root,openPrice,high,low,close,trade_volume,
                                           bid_size,bid,ask_size,ask,implied_underlying_price,
                                           implied_volitility,delta,gamma,theta,vega,rho,opStatic_id,qdt_id)
    
    #insert into underlyings
    putFunc.put_underlying(cur,underlying_bid,underlying_ask,active_underlying_price,qdt_id)
    
