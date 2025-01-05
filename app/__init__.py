# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Brian Liu
# SoftDev
# P02:
# 2024-01-XX
# Time Spent: not enough hours

import random
import os
import sqlite3
import sys
from flask import Flask, render_template, request, session, redirect, url_for, flash
import db
import APIs
import json

DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)

if (not os.path.isfile("geoTracker.db")):
    db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
