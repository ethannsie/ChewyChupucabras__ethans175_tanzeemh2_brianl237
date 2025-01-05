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

if (not os.path.isfile("chupaPokemon.db")):
    db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    passValue = 'username' in session
    print(passValue)
    return render_template("home.html", logged_in = passValue)

@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    db.addUser(username, password)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    if 'username' in session:
        db.updateLoginTime(session['username'])
    return redirect('/')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/chupadex")
def chupadex():
    return render_template("chupadex.html")

@app.route("/ladder")
def ladder():
    return render_template("ladder.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
