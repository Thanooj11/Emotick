#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:20:02 2018

@author: root
"""

from __future__ import print_function
import sys
import requests
from flask import Flask, render_template, request, redirect, url_for

emoji = ''
pid = '1'
app = Flask(__name__)

def postToServer(pid, emoji):
    data = str(pid) + " " + str(emoji)
    r = requests.post("http://localhost:5006", data = data)
    print(r, file = sys.stderr)

@app.route("/", methods = ['GET', 'POST'])
def index():
    global emoji
    if request.method == 'POST':
        print("Posting...", file = sys.stderr)
        if request.form['submit'] == 'Happy':
            emoji = 'happy'
            print("emoji = ", emoji, file = sys.stderr)
        elif request.form['submit'] == 'Okay':
            emoji = 'okay'
            print("emoji = ", emoji, file = sys.stderr)

        elif request.form['submit'] == 'Sad':
            emoji = 'sad'
            print("emoji = ", emoji, file = sys.stderr)
        else:
            print("In else ", file = sys.stderr)
        postToServer(pid, emoji)
        return redirect(url_for(("index")))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True, port = 10005)

            
