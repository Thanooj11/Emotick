#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 13:30:43 2018

@author: root
"""


start_date = "2018-07-26" + ' 00:00'
         
end_date = "2018-07-26" + ' 24:00'
strTest = str("select * from emolog where time >=" + chr(39) + start_date + chr(39) +"and time <" + chr(39) + end_date + chr(39))
print(strTest)