#!/usr/bin/python
# -*- coding: utf-8 -*-

import putFunc
import MySQLdb as mdb
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
from datetime import timedelta

def getcsvD():
    titles = ['underlying_symbol','quote_datetime','root','expiration','strike','option_type','open','high','low','close','trade_volume','bid_size','bid','ask_size','ask','underlying_bid','underlying_ask','implied_underlying_price','active_underlying_price','implied_volatility',	'delta','gamma','theta','vega','rho','hash_value']
    i  = 0 
    csvD = {} #csvDictionary give it a column name and it returns its index 
    for i in range(0, len(titles)): 
        csvD[titles[i]] = i 
    return csvD

def makeFileList(startDate,endDate,directory):
    cDate = startDate 
    fileList = []
    startString = "UnderlyingOptionsIntervalsCalcs_60sec_" 
    endString = ".csv"
    oneDay = timedelta(days=1) #defines a 1day time delta so you can iterate forward one day 
    while(cDate<=endDate): 
        if not ((cDate.weekday()==5) or (cDate.weekday()==6)): #if cDate is saturday or sunday don't do the following thing ADD hol later
            fileName = directory+startString+str(cDate.date())+endString
            fileList.append(fileName)
        cDate = cDate + oneDay
    return fileList

def insertRowDB(row,csvD):
    

    #variables that are inserted into the database
    #quotedt parameters 
    sDateTime = row[csvD['quote_datetime']]
    #option static parameter s
    underlyingSymbol = row[csvD['underlying_symbol']]
    stringExpiration = row[csvD['expiration']]
    strike = row[csvD['strike']]
    option_type = row[csvD['option_type']]
    #dynamic parameters 
    root = row[csvD['root']]
    openPrice = row[csvD['open']]
    high = row[csvD['high']]
    low = row[csvD['low']]
    close = row[csvD['close']]
    trade_volume = row[csvD['trade_volume']]
    bid_size = row[csvD['bid_size']]
    bid = row[csvD['bid']]
    ask_size = row[csvD['ask_size']]
    ask = row[csvD['ask']]
    implied_underlying_price = row[csvD['implied_underlying_price']]
    implied_volitility = row[csvD['implied_underlying_price']]
    delta = row[csvD['delta']]
    gamma = row[csvD['gamma']]
    theta = row[csvD['theta']]
    vega = row[csvD['vega']]
    rho = row[csvD['rho']]
    #underlying parameters
    underlying_bid = row[csvD['underlying_bid']]
    underlying_ask = row[csvD['underlying_ask']]
    active_underlying_price = row[csvD['active_underlying_price']]


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



def addCSVtoDB(csvFileName,csvD): #for clarity of the code this is not generalized and will only work with CBOD database 
    #this is an array of titles that corresponds to the order in the csv files 
    #for example tiles[3] returns a string root 
    #this makes the code much more readable 
    
    titles = ['underlying_symbol','quote_datetime','root','expiration','strike','option_type','open','high','low','close','trade_volume','bid_size','bid','ask_size','ask','underlying_bid','underlying_ask','implied_underlying_price','active_underlying_price','implied_volatility',	'delta','gamma','theta','vega','rho','hash_value']
    j = 0 

    with open(csvFileName, 'rb') as f: #opens the 
        reader = csv.reader(f)
        for row in reader:
            #this processes the string and makes sure each part of the list has the correct datatype 
            if (j ==0):  #skips the first header line 
                j = 1 
                continue 

            #changes the datatype of the elements in the row list 
            #row[csvD['quote_datetime']] = datetime.strptime(row[csvD['quote_datetime']] ,'%Y-%m-%d %H:%M:%S') #these should be changed to datetime64 
            #row[csvD['expiration']] = datetime.strptime(row[csvD['expiration']] +' 16:15:00','%Y-%m-%d %H:%M:%S') #assumes 4:00 est close
            for i in range(csvD['strike'],csvD['rho']+1): #turns all of the float rows into floats 
                if i != csvD['option_type']: #avoids the option time column when trying to float convert 
                    row[i] = float(row[i])
            
            insertRowDB(row,csvD)


def main_func():
    startDate = datetime.strptime("2009-03-20","%Y-%m-%d") #inclusive 
    endDate = datetime.strptime("2009-03-31","%Y-%m-%d") #inclusive 
    directory = "/home/dexter/data/"
    csvD = getcsvD()
    fileList = makeFileList(startDate,endDate,directory)

    #overrides filelist to speedup code for testing purposes 
    #fileList = ["C:/data/newTest.csv"]
    for csvFileNames in fileList: 
        print "reading file " + csvFileNames 
        optionD = addCSVtoDB(csvFileNames,csvD)

main_func()

        
