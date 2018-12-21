#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:11:48 2018

@author: root
"""

from __future__ import print_function
from flask import Flask, Response, request
import sys
import psycopg2
from psycopg2.extensions import AsIs


app = Flask(__name__)

def writeToFile(datas):
    conn = psycopg2.connect(database="emotick", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    f = open('Database.txt','a')
    if len(datas)!=0:
        lists = datas.split(" ")
        print(len(lists), file = sys.stderr)
        if lists:
            print(lists, file = sys.stderr)
            f.write(str(len(lists[0])))
            cur.execute("INSERT into emotickschema.table1 (id,happy,okay,sad) select '%s','0','0','0' where not exists (SELECT * FROM emotickschema.table1 where id = %s)",(AsIs(lists[0]),AsIs(lists[0])))
            conn.commit()
            cur.execute("UPDATE emotickschema.table1 SET %s  = %s + 1  where id = %s",(AsIs(lists[1]), AsIs(lists[1]), AsIs(lists[0])))
        else:
            print("list is empty", file = sys.stderr)
    conn.commit()
    conn.close()

@app.route('/', methods = ['POST', 'GET'])
def get_data():
    data = request.data
    writeToFile(data)
    print("Data = ", data, file = sys.stderr)
    return Response(request.data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='176.23.28.226', port= 5006)
