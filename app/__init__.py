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
import gameFunctions
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
db.setup()
counter_initialized = False

def initialize_counter():
    global counter_initialized
    if not counter_initialized:
        db.resetChallenge()
        print(db.getTable("gameChallenge"))
        counter_initialized = True

# Call this function at the appropriate place in your Flask app
initialize_counter()

@app.route("/", methods=['GET', 'POST'])
def home():
    print(db.getTable("users"))
    passValue = 'username' in session
    if 'username' in session:
        if db.getTableData("users", "username", session['username'])[4] != "No":
            return redirect("/game")
        challenges = db.getAllTableData("gameChallenge", "challenged", session['username'])
        updateChallenges = []
        passUsers = {}
        for user in active_sessions:
            if user != session['username']:
                passUsers[user] = db.getUserID(session['username'])
        if challenges == -1:
            return render_template("home.html", logged_in = passValue, username=session['username'], activeUsers=passUsers, mode = mode)
        for count, challenge in enumerate(challenges):
            if challenge[3] == 'None':
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
    challenge_data = []
    if passValue:
        challenge_data = db.getChallengeHistory(session['username'])
        challenge_data.append(db.getChallengeHistory(session['username']))
    return render_template("history.html", mode = mode, logged_in = passValue, challenge_data = challenge_data[:len(challenge_data)-1])

@app.route("/game", methods=['GET', 'POST'])
def game():
    game_id = db.getTable("gameHistory")
    passValue = 'username' in session
    if 'username' in session:
        if db.getTableData("users", "username", session['username'])[4] != "No":
            #ISSUE: moves that dont do dmg actually just dont do anything
                #Variable Setup
            p1_user = db.getLatestChallenge()[1]
            p2_user = db.getLatestChallenge()[2]
            game_id = db.getLatestGameHistory()[0]
            p1_active = gameFunctions.getCurrActivePokemon(game_id, p1_user)
            p2_active = gameFunctions.getCurrActivePokemon(game_id, p2_user)
            p1_sprite = gameFunctions.getPokeSprite(p1_active)
            p2_sprite = gameFunctions.getPokeSprite(p2_active)
            p1_active_hp = gameFunctions.getActivePokemonHP(game_id, p1_user)
            p2_active_hp = gameFunctions.getActivePokemonHP(game_id, p2_user)
            db.updateBattleLog(game_id, " ")
            battlelog = db.getTableData("battlelog", "game_ID", game_id)

            # ISSUE: MAKE SURE YOU ACTUALLY NEED TO MAKE A NEW TURN-- same code to check if a turn has passed
            db.initializeGameTracker(game_id)

            #Returns moves available to the active pokemon and pokemon available to be swapped to
            if session['username'] == p1_user:
                activePokeMoves = gameFunctions.getActivePokemonMoves(game_id, p1_user)
                inactivePokemon = gameFunctions.getInActivePokemon(game_id, p1_user)
            elif session['username'] == p2_user:
                activePokeMoves = gameFunctions.getActivePokemonMoves(game_id, p2_user)
                inactivePokemon = gameFunctions.getInActivePokemon(game_id, p2_user)
            #Auto Swaps when active pokemon has fainted
            if gameFunctions.getActivePokemonHP(game_id, p1_user) <= 0:
                if (gameFunctions.getAlivePokemon(game_id, p1_user)):
                    gameFunctions.swapPokemon(game_id, p1_user, gameFunctions.getAlivePokemon(game_id, p1_user)[0])
                    db.updateBattleLog(game_id, p1_active + "has fainted! Swap to your next chupamon!")
                    return redirect('/game')
                else:
                    db.updateGameHistory(game_id, p2_user, p1_user, "idk")
                    db.updateBattleLog(game_id, p1_user + "has lost! " + p2_user + " is the winner!")
                    gameFunctions.updateElo(game_id)
                    db.resetUsers(p1_user, p2_user)
                    return redirect('/')
            if gameFunctions.getActivePokemonHP(game_id, p2_user) <= 0:
                if (gameFunctions.getAlivePokemon(game_id, p2_user)):
                    gameFunctions.swapPokemon(game_id, p2_user, gameFunctions.getAlivePokemon(game_id, p2_user)[0])
                    db.updateBattleLog(game_id, p2_active + "has fainted! Swap to your next chupamon!")
                    return redirect('/game')
                else:
                    db.updateGameHistory(game_id, p1_user, p2_user, "idk")
                    db.updateBattleLog(game_id, p2_user + "has lost! " + p1_user + " is the winner!")
                    gameFunctions.updateElo(game_id)
                    db.resetUsers(p1_user, p2_user)
                    return redirect('/')
            #Handles User inputs

            if session['username'] == p1_user:
                #Surrendering
                if request.form.get('form_type') == "surrender":
                    # Put message in battle log that user surrendered
                    db.updateBattleLog(game_id, p1_user + "has surrendered")
                    db.updateGameHistory(game_id, p2_user, p1_user, "idke")
                    gameFunctions.updateElo(game_id)
                    return redirect('/')
                #Swapping Pokemon
                if request.form.get('form_type') == "swap":
                    gameFunctions.swapPokemon(game_id, p1_user, request.form['poke_name'])
                    db.updateBattleLog(game_id, p1_user + " has swapped " + p1_active + " for " + request.form['poke_name'])
                    # GET THE TURN FROM THE GAMETRACKER AND ALSO INCREMENT IT
                    db.updateGameTracker(game_id, session['username'], "swap", 1, )
                #Attacking
                if request.form.get('form_type') == "attack":
                    damage = gameFunctions.damageCalc(request.form['move_name'], p1_active, p2_active)
                    db.updateBattleLog(game_id, p1_active + "has dealt " + str(damage) + " damage to " + p2_active)
                    gameFunctions.updateActiveHP(game_id, p2_user, p2_active, damage)
                    db.updateGameTracker(game_id, session['username'], "attack", 1, )
            if session['username'] == p2_user:
                #Surrendering
                if request.form.get('form_type') == "surrender":
                    # Put message in battle log that user surrendered
                    db.updateBattleLog(game_id, p2_user + "has surrendered")
                    db.updateGameHistory(game_id, p1_user, p2_user, "idk")
                    gameFunctions.updateElo(game_id)
                    db.resetUsers(p1_user, p2_user)
                    return redirect('/')
                #Swapping Pokemon
                if request.form.get('form_type') == "swap":
                    db.updateBattleLog(game_id, p2_user + " has swapped " + p2_active + " for " + request.form['poke_name'])
                    gameFunctions.swapPokemon(game_id, p2_user, request.form['poke_name'])
                #Attacking
                if request.form.get('form_type') == "attack":
                    damage = gameFunctions.damageCalc(request.form['move_name'], p2_active, p1_active)
                    db.updateBattleLog(game_id, p2_active + "has dealt " + str(damage) + " damage to " + p1_active)
                    gameFunctions.updateActiveHP(game_id, p1_user, p1_active, damage)

            return render_template("game.html",
                                       username1 = p1_user, username2 = p2_user, poke1Name = p1_active, poke2Name = p2_active, sprite1 = p1_sprite, sprite2 = p2_sprite,
                                       pokeMoves = activePokeMoves, inactivePokemon = inactivePokemon,
                                       hp1 = p1_active_hp, hp2 = p2_active_hp, mode=mode, logged_in=passValue,
                                       battlelog = battlelog)
    flash("You have not yet accepted a game challenge", 'error')
    return redirect('/')

@app.route("/challenge", methods=['GET', 'POST'])
def challenge():
    if 'username' in session and session['username'] != request.form['username']:
        db.updateChallengeInitial(session['username'], request.form['username'])
        if db.getChallengeData("None", session['username'], request.form['username']) != -1 and len(db.getChallengeData("None", session['username'], request.form['username'])) > 1:
            db.deleteChallenge(session['username'], request.form['username'])
        if 'username' not in session:
            flash("You need to challenge users through the menu", 'error')
    return redirect('/')

@app.route("/accept_your_fate", methods=['GET', 'POST'])
def accept_your_fate():
    if 'username' in session and request.form != None:
        if db.getChallengeData("None", request.form['username'], session['username']) != -1:
            db.updateChallengeFinal("Yes", request.form['username'], session['username'])
            db.setTableData("users", "in_game", request.form['username'], "username", session['username'])
            db.setTableData("users", "in_game", session['username'], "username", request.form['username'])
            gameFunctions.startgame(db.getLatestChallenge()[1], db.getLatestChallenge()[2])
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
