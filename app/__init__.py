# ChewyChupucabras - Tanzeem Hasan, Ethan Sie, Brian Liu
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
import game
import APIs
import json

DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)
active_sessions = {}

if (not os.path.isfile("chupaPokemon.db")):
    db.setup() # sets up databases
    APIs.fetch_poke()
    APIs.fetch_moves()
    print(db.getTable("pokeDex"))


@app.route("/", methods=['GET', 'POST'])
def home():
    passValue = 'username' in session
    print(db.getTable("users"))
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
    password2 = request.form.get('password2')

    if password != password2:
        flash("Passwords do not match", 'error')
        return redirect("/")
    elif db.getUserID(username) >= 0:
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

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        flash("Logged out", 'success')
        active_sessions.pop(session['username'])
        session.pop('username', None)
    return redirect("/")

@app.route("/chupadex", methods=['GET', 'POST'])
def chupadex():
    return render_template("chupadex.html", pokemon_data=db.getTable("pokeDex"))

@app.route("/ladder", methods=['GET', 'POST'])
def ladder():
    data = db.getTable("users")
    userData = []
    rankData = []
    for user in data:
        if [user[0], user[1], user[3]] not in userData:
            userData.append([user[0], user[1], user[3]])
            rankData.append(user[3])
    rankData.sort(reverse=True)
    passData = []
    for rank in rankData:
        for count, user in enumerate(userData):
            if rank == user[2]:
                passData.append([user[0],user[1],user[2]])
                userData.pop(count)

    return render_template("ladder.html", user_data=passData)

@app.route("/history", methods=['GET', 'POST'])
def history():
    return render_template("history.html")

@app.route("/game", methods=['GET', 'POST'])
def game():
    return render_template("game.html")

@app.route("/challenge", methods=['GET', 'POST'])
def challenge():
    db.updateChallengeInitial(session['username'], request.form['username'])
    return redirect('/')

@app.route("/accept_your_fate", methods=['GET', 'POST'])
def accept_your_fate():
    if getTableData("gameChallenge", "accepted_status", "challenger", session['user']) != None and getTableData("gameChallenge", "accepted_status", "challenged", request.form['user']) != None:
        db.updateChallengeFinal("Yes", request.form['username'], session['username'])
    return redirect('/')

@app.route("/reject_your_fate", methods=['GET', 'POST'])
def reject_your_fate():
    if getTableData("gameChallenge", "accepted_status", "challenger", session['user']) != None and getTableData("gameChallenge", "accepted_status", "challenged", request.form['user']) != None:
        db.updateChallengeFinal("No", request.form['username'], session['username'])
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()
