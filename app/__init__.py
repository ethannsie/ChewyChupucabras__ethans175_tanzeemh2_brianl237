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
## False = Dark mode, True = Light Mode
mode = False
app.secret_key = os.urandom(32)
active_sessions = {}

#os.remove("chupaPokemon.db")
if (not os.path.isfile("chupaPokemon.db")):
    db.setup() # sets up databases
    APIs.fetch_poke()
    APIs.fetch_moves()
    APIs.fetch_type()


#print(db.getTable("types"))


@app.route("/", methods=['GET', 'POST'])
def home():
    passValue = 'username' in session
    if 'username' in session:
        challenges = db.getAllTableData("gameChallenge", "challenged", session['username'])
        updateChallenges = []
        passUsers = {}
        print(challenges)
        for user in active_sessions:
            if user != session['username']:
                passUsers[user] = db.getUserID(session['username'])
        if challenges == -1:
            return render_template("home.html", logged_in = passValue, username=session['username'], activeUsers=passUsers, mode = mode)
        for count, challenge in enumerate(challenges):
            if challenge[3] == None:
                updateChallenges.append(challenge)
        return render_template("home.html", logged_in = passValue, username=session['username'], activeUsers=passUsers, challenges=updateChallenges, mode = mode)
    return render_template("home.html", logged_in = passValue, mode = mode)

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
    passValue = 'username' in session
    search_query = request.args.get('search')
    stat = request.args.get('stat')
    operator = request.args.get('operator')
    value = request.args.get('value')

    pokemon_data = None
    search = 1
    if search_query:
        # Check if the search query is numeric (search by ID) or alphabetic (search by name)
        if search_query.isdigit():
            result = db.getTableData("pokeDex", "poke_ID", search_query)
            if result != -1:
                pokemon_data = result
            search = 2
        else:
            result = db.getPokeData("pokeDex", "poke_name", search_query)
            if result != -1:
                pokemon_data = result
            search = 2
    elif stat and operator and value:
        if stat in ["HP", "ATK", "DEF", "SpATK", "SpDEF", "SpE"] and operator in [">", "<", ">=", "<="]:
            pokemon_data = db.getStatFilteredData("pokedex", stat, operator, value)
    else:
        # If no search query, display all Pokémon
        pokemon_data = db.getTable("pokeDex")  # This will select all rows
        search = 1
    return render_template("chupadex.html", pokemon_data=pokemon_data, search=search, logged_in = passValue, mode=mode)

@app.route("/ladder", methods=['GET', 'POST'])
def ladder():
    passValue = 'username' in session
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

    return render_template("ladder.html", user_data = passData, mode = mode, logged_in = passValue)

@app.route("/history", methods=['GET', 'POST'])
def history():
    passValue = 'username' in session
    return render_template("history.html", mode = mode, logged_in = passValue)

@app.route("/game", methods=['GET', 'POST'])
def game():
    if 'username' in session: # this needs to be updated only redirect to game.html if there is an active challenge accepted on the user

        # todo: battlelog
        # if attack, then print "Your poke_name used poke_move! It's "
        return render_template("game.html", mode=mode)
    return redirect('/')

@app.route("/challenge", methods=['GET', 'POST'])
def challenge():
    if 'username' in session:
        try:
            db.updateChallengeInitial(session['username'], request.form['username'])
        except:
            flash("You need to challenge users through the menu", 'error')
    return redirect('/')

@app.route("/accept_your_fate", methods=['GET', 'POST'])
def accept_your_fate():
    if 'username' in session and request.form != None:
        if db.getChallengeData("None", "challenged", session['username']) == None and db.getChallengeData("None", "challenger", request.form['username']) == None:
            print("please work")
            db.updateChallengeFinal("Yes", request.form['username'], session['username'])
            return redirect('/game')
    return redirect('/')

@app.route("/mode_swap", methods=['GET', 'POST'])
def mode_swap():
    global mode
    mode = not mode
    return redirect('/')

# @app.route("/reject_your_fate", methods=['GET', 'POST'])
# def reject_your_fate():
#     if getTableData("gameChallenge", "accepted_status", "challenger", session['user']) != None and getTableData("gameChallenge", "accepted_status", "challenged", request.form['user']) != None:
#         db.updateChallengeFinal("No", request.form['username'], session['username'])
#     return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run()
