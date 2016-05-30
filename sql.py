# -*- coding: utf-8 -*-
# sql.py - Create a SQLite3 table and populate it with data
"""
Created on Sun May 29 22:02:46 2016
@author: Tom
"""

import sqlite3

# create a new database if the db doesn't already exist
with sqlite3.connect("blog.db") as connection:
    # get a cursor object to execute SQL commands
    c = connection.cursor()
    
    # create the table
    c.execute("""CREATE TABLE posts
                (title TEXT, post TEXT)
                """)
    
    # insert dummy data into the table
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
    c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
    c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay.")')
    