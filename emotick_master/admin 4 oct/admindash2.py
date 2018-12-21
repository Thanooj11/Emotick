#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 15:19:07 2018

@author: root
"""

from __future__ import print_function



from flask import Flask, Response, request, render_template, redirect, url_for



import sys



import psycopg2



from psycopg2.extensions import AsIs

happyq1 = 0

sadq1 = 0

okayq1 = 0

app = Flask(__name__)

@app.route('/addQuestion', methods = ['POST', 'GET'])
    
def addQuestion():
    
    conn = psycopg2.connect(database="emotickdatabase", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")
    
    cur = conn.cursor()
    
    cur.execute("select * from category_table")
    
    row = cur.fetchall()
    
    length = len(row)
    
    return render_template('index2.html',row = row, length = length)
    
    
         
    
    


@app.route('/submit', methods = ['POST', 'GET'])
    
def submit():
     
     global happyq1
     
     global sadq1
     
     global okayq1
    
     location = request.form['location']     
     
     room = request.form['room']
     
     building = request.form['building']
     
     start_date = request.form['sdate']
     
     end_date = request.form['edate']
     
     start_time = request.form['stime']
     
     end_time = request.form['etime']
     
     if start_time == '':
         start_time = ' 00:00'
     else:
         start_time = ' ' + start_time 
         
     if end_time == '':
         end_time = ' 24:00'
     else:
         end_time = ' ' + end_time
     if start_date!='' and end_date!='':
     
         start_date = start_date + start_time
             
         end_date = end_date + end_time
         
         question = request.form['qid']  
         
         conn = psycopg2.connect(database="emotickdatabase", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")
    
         cur = conn.cursor()
         
         cur.execute("select qid from question_table where question = '%s' ", (AsIs(question),))
         
         row = cur.fetchall()
         
         qid = row[0]
        
         happyq1 = 0
         
         sadq1 = 0
         
         okayq1 = 0
             
         cur.execute("select cid from category_table where cid in (select category_table.cid from category_table join (select * from category_question where qid = %s) t1 on t1.cid = category_table.cid) and (city like %s or state like %s or country like %s) or building like %s ", ((qid),(location)+"%",(location)+"%",(location)+"%",(building)+"%",))
         
         row = cur.fetchall()
         
         for i in range(len(row)):
             cid = row[i]
    
             cur.execute("select * from emolog where emolog.id in (select id from device_category where cid = %s ) and type_of_room like %s and (time >=%s and time < %s)",((cid),(room)+"%",(start_date),(end_date),))
    
             rows = cur.fetchall()
         
             for i in range(len(rows)):
                 emotion = rows[i][1]
         
                 if emotion == 'Happy':
                     happyq1 = happyq1 + 1
                 elif emotion == 'Okay':
                     okayq1 = okayq1 + 1
                 elif emotion == 'Sad':
                     sadq1 = sadq1 + 1
     else:
         
         question = request.form['qid']  
         
         conn = psycopg2.connect(database="emotickdatabase", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")
    
         cur = conn.cursor()
         
         cur.execute("select qid from question_table where question = '%s' ", (AsIs(question),))
         
         row = cur.fetchall()
         
         qid = row[0]
        
         happyq1 = 0
         
         sadq1 = 0
         
         okayq1 = 0
             
         cur.execute("select cid from category_table where cid in (select category_table.cid from category_table join (select * from category_question where qid = %s) t1 on t1.cid = category_table.cid) and (city like %s or state like %s or country like %s) and building like %s ", ((qid),(location)+"%",(location)+"%",(location)+"%",(building)+"%",))
         
         row = cur.fetchall()
         
         for i in range(len(row)):
             cid = row[i]
    
             cur.execute("select * from emolog where emolog.id in (select id from device_category where cid = %s ) and type_of_room like %s ",((cid),(room)+"%",))
    
             rows = cur.fetchall()
         
             for i in range(len(rows)):
                 emotion = rows[i][1]
         
                 if emotion == 'Happy':
                     happyq1 = happyq1 + 1
                 elif emotion == 'Okay':
                     okayq1 = okayq1 + 1
                 elif emotion == 'Sad':
                     sadq1 = sadq1 + 1
             
     return redirect(url_for('indexResult'))
     
     
@app.route('/result', methods = ['POST', 'GET'])

def indexResult():
    
   global happyq1 

   global sadq1
   
   global okayq1  

   return render_template('index2.html', happy = happyq1, sad = sadq1, okay = okayq1)


@app.route('/', methods = ['POST', 'GET'])



def index():

   global happyq1 

   happy = 0

   

   sad = 0

   

   okay = 0

   

   conn = psycopg2.connect(database="emotickdatabase", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")



   cur = conn.cursor()

    

   #cur.execute("INSERT into emotick(id,happy,okay,sad) select '%s','0','0','0' where not exists (SELECT * FROM emotick where id = %s)",(1,1))



   cur.execute("select * from emotick")

   

   rows = cur.fetchall()

   

   for row in rows:

       

       happy = happy + row[1]

       

       okay = okay + row[2]

       

       sad = sad + row[3]
       

   conn.commit()



   conn.close()

   

   return render_template('index2.html', happy = happy, sad = sad, okay = okay , happyq1 = happyq1)



if __name__ == '__main__':



    app.run(debug=True, threaded=True, port= 5009, host='176.23.8.211')
