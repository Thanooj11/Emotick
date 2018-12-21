#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:12:21 2018

@author: root
"""

from __future__ import print_function



from flask import Flask, Response, request, render_template



import sys



import psycopg2



from psycopg2.extensions import AsIs



app = Flask(__name__)



@app.route('/', methods = ['POST', 'GET'])
def index():
    conn = psycopg2.connect(database="emotick", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("select * from emolog where id = %s and  emotion = %s", (AsIs('1043'),AsIs('Happy'),));
    rows = cur.fetchall()
    return render_template('index1.html')


if __name__ == '__main__':
    app.run(debug=True, port= 5011, host='176.23.28.183')