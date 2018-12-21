#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 13:16:25 2018

@author: root
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:31:52 2018

@author: root
"""

# before changing to yag all commented

from __future__ import print_function

from flask import Flask, request,render_template

from flask_mail import Mail, Message

import sys

import psycopg2

from psycopg2.extensions import AsIs

from datetime import datetime

import sched, time

import yagmail

import os


question=""
rows=''
mg ="check"
start_var = 0

heartbeatCount = {}

heartbeatCount[1041] = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")

deviceList = [1041]


app = Flask(__name__)


app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'sender123flask@gmail.com',
    MAIL_PASSWORD = 'admin123flask#',
    MAIL_DEFAULT_SENDER ='sender123flask@gmail.com'
    
))

mail = Mail(app)

def raiseAlert(device_id):
#    
    f = open('alert.txt','a+')
#    
    f.write(str(device_id))
#    
    f.write(" ")
#    
    f.write(str(heartbeatCount[device_id]))
#    
    f.write("\n")
##    
    f.close()
#    print("tada")
#    msg = Message('Alert', recipients = ['pkalyanimenon@gmail.com'])
##    
#    msg.body = "This is the email body" + str(device_id)
##    
#    mail.send(msg)
    yag = yagmail.SMTP("sender123flask@gmail.com")
    contents = "Device down" + str(device_id)
    yag.send("thanoojdigi@gmail.com", "Alert", contents)
    

@app.route('/check_heartbeat', methods=['GET', 'POST'])
def check_heartbeat():
    
    global start_var
    global mg
    
    if start_var == 0:
    
        #app.run(debug=True, port= 7006, threaded=True, host = '176.23.5.19')
#        start_var = start_var + 1
#        time.sleep(5)
        start_var = 1   
    
        
    
#    if start_var == 0:
#        msg = Message('Alert', recipients = ['pkalyanimenon@gmail.com'])
#        msg.body = "This is the email body" + str(1041)
#        mg = str(msg.body)
#        mail.send(msg)
#    else:
#        mg = "hai" + str(start_var)
    
#    msg.body = "This is the email body" + str(1041)
    
#    mail.send(msg)
    
    f = open('check.txt','a')
    
    f.write("hi")
    
    f.close()
    
    if start_var != 0:
        raiseAlert(1041)
        f = open('check.txt','a')
    
        f.write("hai")
        f.flush()
        f.close()
#    time.sleep(10)
#    check_heartbeat()
#    s.enter(30, 1, check_heartbeat, (s,))

    
    for i in range(len(deviceList)):
        
        device_id = deviceList[i]
        
        time = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
        
        difference = time - heartbeatCount[device_id]
        
        if float( str(difference)[5:] ) <= 15:
#        if device_id == 1041:  
            raiseAlert(device_id)
    
#    s = sched.scheduler(time.time, time.sleep)
#
    #sc.enter(30, 1, check_heartbeat, (sc,))
#    
#    s.enter(30, 0, check_heartbeat())
#    s.run()            

@app.route('/heart_beat', methods=['GET', 'POST'])
def heart_beat():
    
    global question
    
    global rows
    
    data = request.data

    f = open('database.txt','a')
    
    f.write(data)
    
    lists = data.split(" ")
    
    device_id = lists[0]
    
    room_type = lists[1]
    
    heartbeatCount[device_id] = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
    
    f.write(str(datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")))
    
    f.write("\n")
    
    f.close()
    
    return render_template("index.html", question = question , rows =rows)    


#
@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    
    global question
    
    global rows
    
    return render_template("thank_you.html")


# render the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    
    global question
    
    global rows
    
    
    return render_template("index.html", question = question, rows = rows)


#to get the response
@app.route('/data', methods=['GET', 'POST'])
def data_post():
    
    global question
    
    global rows
    
    data = request.data

    writeToDb(data)

    print("Data = ", data, file = sys.stderr)
    
    return render_template("index.html", question = question , rows =rows) 
    #return render_template("thank_you.html")#-------------->changed   


def writeToDb(datas):

    conn = psycopg2.connect(database="emotick", user = "postgres", password = "password123", host = "127.0.0.1", port = "5432")

    cur = conn.cursor()
    
    global question
    
    global rows
    
    if len(datas)!=0:

        lists = datas.split(" ")

        print(len(lists), file = sys.stderr)

        if lists:

            print(lists, file = sys.stderr)
            
            emotion = lists[0]

            device_id = lists[1]
            
            type_of_room = lists[2]
            

            cur.execute("INSERT into emotickschema.table1 (id,happy,okay,sad) select '%s','0','0','0' where not exists (SELECT * FROM emotickschema.table1 where id = %s)",(AsIs(lists[1]),AsIs(lists[1])))

            conn.commit()

            cur.execute("UPDATE emotickschema.table1 SET %s  = %s + 1  where id = %s",(AsIs(emotion), AsIs(emotion), AsIs(device_id),))
            
            conn.commit()
            
            cur.execute("select cid from device_category where id = %s ",(AsIs(device_id),))
            
            row1 = cur.fetchone()
            
            cid = row1[0]
            
            cur.execute("SELECT question from question_table INNER JOIN category_question ON (question_table.qid = category_question.qid) AND cid = %s ",(AsIs(cid),))
            
            rows = cur.fetchone()
            
            question = rows[0] 
            
            conn.commit()
            
            cur.execute("select qid from question_table where question = '%s' ", (AsIs(question),))
            
            row = cur.fetchone()
            
            qid = row[0]
            
            conn.commit()
            
            cur.execute("INSERT into emolog (id,emotion,type_of_room,qid) select '%s','%s','%s', '%s' ",(AsIs(device_id),AsIs(emotion),AsIs(type_of_room),AsIs(qid),))
                        
        else:

            print("list is empty", file = sys.stderr)
            

    conn.commit()

    conn.close()


if __name__ == '__main__':
    
    
    #s = sched.scheduler(time.time, time.sleep)

    #s.enter(1, 1, check_heartbeat, (s,))
#    
    #s.run()
#    app1.run(debug = True,host = '176.23.5.19', port = 7011)
#    s = sched.scheduler(time.time, time.sleep)
#    s.run()
#    check_heartbeat()
#    s.enter(10, 1, check_heartbeat, (s,))
    app.run(debug=True, port= 7005, threaded=True, host = '176.23.5.19')

