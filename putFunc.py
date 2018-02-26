#!/user/bin/python
# -*- coding: utf-8 -*-
#import MySQLdb as mdb

#note to self. It might be a good idea to create a flush cursor option
#in each of these functinos. The current setup probably creates errors

def lastInsertId(cur):
    cur.execute("SELECT LAST_INSERT_ID()")
    return cur.fetchall()[0][0] #returns the last insert id, i.e the dt id

def put_expiration(cur,sDateTime):
    cur.execute("SELECT id FROM expiration WHERE dt = %s",(sDateTime,))
    ids = cur.fetchall()
    if not ids:
        cur.execute("INSERT INTO expiration( dt ) VALUES( %s )",(sDateTime,))
    else:
       return ids[0]

    #get the new id
    return lastInsertId(cur)

def put_dt(cur,sDateTime):
    cur.execute("SELECT id FROM quotedt WHERE dt = %s",(sDateTime,))
    ids = cur.fetchall()
    if not ids:
        cur.execute("INSERT INTO quotedt( dt ) VALUES( %s )",(sDateTime,))
    else:
       return ids[0]

    #get the new id
    return lastInsertId(cur)

def put_opStatic(cur, symbol,sExpiration,strike,opType,expiration_id):
    cur.execute("SELECT id FROM opStaticPs WHERE underlyingSymbol = %s AND expiration = %s" \
                "AND strike = %s AND op_type = %s",(symbol,sExpiration,strike,opType,))
    ids = cur.fetchall()
    if not ids:
        cur.execute("INSERT INTO opStaticPs(underlyingSymbol,expiration,strike,op_type,expiration_id) "\
                    "VALUES(%s,%s,%s,%s,%s)",(symbol,sExpiration,strike,opType,expiration_id,))
    else:
        return ids[0]

    return lastInsertId(cur)  #returns the last insert id, i.e the dt id


def put_opDynamic(cur,root,openPrice,high,low,close,trade_volume,bid_size,bid,ask_size,ask,implied_underlying_price,implied_volitility,delta,gamma,theta,vega,rho,opStatic_id,qdt_id):

    cur.execute("INSERT INTO opDynamicPs(root,open,high,low,close,trade_volume," \
            "bid_size,bid,ask_size,ask,implied_underlying_price,implied_volitility,"\
            "delta,gamma,theta,vega,rho,opStaticPs_id,quotedt_id)"
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"\
            "%s,%s,%s,%s)",(root,openPrice,high,low,close,trade_volume,
                            bid_size,bid,ask_size,ask,implied_underlying_price,
                            implied_volitility,delta,gamma,theta,vega,rho,opStatic_id,qdt_id,))

    return lastInsertId(cur)

def put_underlying(cur,underlying_bid,underlying_ask,active_underlying_price,qdt_id):
    cur.execute("SELECT id FROM underlyings WHERE quotedt_id = %s",(qdt_id,))
    ids = cur.fetchall()
    if not ids:
        cur.execute("INSERT INTO underlyings(underlying_bid,underlying_ask,active_underlying_price,quotedt_id)"\
                "VALUES(%s,%s,%s,%s)",(underlying_bid,underlying_ask,active_underlying_price,qdt_id,))
    else:
        return ids[0] 
    
    return lastInsertId(cur) 
