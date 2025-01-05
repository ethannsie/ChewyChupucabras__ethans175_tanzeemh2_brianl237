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
active_sessions = {}

if (not os.path.isfile("chupaPokemon.db")):
    db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    passValue = 'username' in session
    print(active_sessions)
    if 'username' in session:
        passUsers = {}
        for user in active_sessions:
            if user != session['username']:
                passUsers[user] = db.getUserID(session['username'])
        return render_template("home.html", logged_in = passValue, username=session['username'], activeUsers=passUsers)
    return render_template("home.html", logged_in = passValue)

@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if db.getUserID(username) >= 0:
        flash("Username already exists", 'error')
        return redirect("/")
    else:
        session['username'] = username
        active_sessions[session['username']] = db.getUserID(session['username'])
        flash("Registered Sucessfully!", "success")
        db.addUser(username, password)
        return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in active_sessions:
        flash("You already have an active session.", 'error')
    elif db.getUserID(username) >= 0 and db.getTableData("users", "username", username)[2] == password:
        session['username'] = username
        active_sessions[session['username']] = db.getUserID(session['username'])
        db.updateLoginTime(session['username'])
        flash("Logged in", 'success')
    else:
        flash("Incorrect username or password.", 'error')
    return redirect("/")

@app.route("/logout")
def logout():
    if 'username' in session:
        flash("Logged out", 'success')
        active_sessions.pop(session['username'])
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
