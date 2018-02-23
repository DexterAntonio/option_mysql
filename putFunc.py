#!/user/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb


def put_dt(cur,sDateTime):
    cur.fetchall()
    cur.execute("SELECT id FROM quotedt WHERE dt = %s",(sDateTime,))
    ids = cur.fetchall()
    if not ids:
        cur.execute("INSERT INTO quotedt( dt ) VALUES( %s )",(sDateTime,))
    else:
       return ids[0]

    #get the new id 
    cur.execute("SELECT LAST_INSERT_ID()")
    return cur.fetchall()[0][0] #returns the last insert id, i.e the dt id



