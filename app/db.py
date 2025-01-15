# ChewyChupucabras - Tanzeem Hasan, Ethan Sie, Brian Liu
# SoftDev
# P02:
# 2024-01-XX
# Time Spent: not enough hours

import sqlite3
import csv
from datetime import datetime

DB_FILE = "chupaPokemon.db"

def setup():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, rank INTEGER, in_game TEXT, created_at TEXT, last_login TEXT);")
    # Database holds all of the pokemon information for gen1; allows 6 pokemons to be chosen
    c.execute("CREATE TABLE IF NOT EXISTS pokeDex (poke_ID INTEGER PRIMARY KEY AUTOINCREMENT, poke_name TEXT, type_1 TEXT, type_2 TEXT, HP INTEGER, ATK INTEGER, DEF INTEGER, SpATK INTEGER, SpDEF INTEGER, SpE INTEGER, sprite_url TEXT);")
    # Integrate both of them together to randomly select the 4 moves each pokemon will get
    c.execute("CREATE TABLE IF NOT EXISTS moves (id INTEGER PRIMARY KEY, name TEXT, type TEXT, power INTEGER, accuracy INTEGER, pp INTEGER, class_type TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS pokemon_moves (poke_name TEXT, move_id INTEGER);")
    # Database holds all of the pokemon types with their type matchups
    c.execute("CREATE TABLE IF NOT EXISTS types (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, double_dmg_from TEXT, double_dmg_to TEXT, half_dmg_from TEXT, half_dmg_to TEXT, no_dmg_from TEXT, no_dmg_to TEXT);")


    # Database to track what games are being challenged
    c.execute("CREATE TABLE IF NOT EXISTS gameChallenge (challenge_ID INTEGER PRIMARY KEY AUTOINCREMENT, challenger TEXT, challenged TEXT, accepted_status TEXT);")
    # Creates game_id (marks the start of the game) and tracks end results of each game, will also act as the main match history database
    c.execute("CREATE TABLE IF NOT EXISTS gameHistory (game_ID INTEGER PRIMARY KEY, winner TEXT, loser TEXT, time_started TEXT, time_completed TEXT);")
    # Database keeps track of all six collection of pokemons from each game
    c.execute("CREATE TABLE IF NOT EXISTS gamePokeSets (game_ID INTEGER PRIMARY KEY, user TEXT, poke1 TEXT, poke2 TEXT, poke3 TEXT, poke4 TEXT, poke5 TEXT, poke6 TEXT);")
    # Database keeps track of the health of all six collection of pokemons from each game (active_status = True if active, otherwise False)
    c.execute("CREATE TABLE IF NOT EXISTS gamePokeStats (game_ID INTEGER, user TEXT, poke_name TEXT, active_hp REAL, active_status TEXT, move1 INTEGER, move2 INTEGER, move3 INTEGER, move4 INTEGER);")
    # Tracks the game once it's begun, will make a new entry to track every turn between two players
    c.execute("CREATE TABLE IF NOT EXISTS gameTracker (game_ID INTEGER PRIMARY KEY, player1 TEXT, player2 TEXT, move1 TEXT, move2 TEXT, turn INTEGER);")

    db.commit()
    db.close()

def addUser(username, password):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # datetime formatting for sqlite text
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # omits userID as an input as it autoincrements
    c.execute("INSERT INTO users (username, password, rank, in_game, created_at, last_login) VALUES (?, ?, ?, ?, ?, ?)", (username, password, 1000, "No", created_at, created_at))
    db.commit()
    db.close()

def updateLoginTime(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    userID = getUserID(username)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE users SET last_login = ? WHERE user_id = ?", (current_time, userID))
    db.commit()
    db.close()

# searches the users DB for the userID associated to the username parameter
def getUserID(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result[0]
    else:
        return -1

def updatePokeList(name, type_1, type_2, hp, attack, defense, special_attack, special_defense, speed, sprite_url):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO pokeDex (poke_name, type_1, type_2, HP, ATK, DEF, SpATK, SpDEF, SpE, sprite_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, type_1, type_2, hp, attack, defense, special_attack, special_defense, speed, sprite_url))
    db.commit()
    db.close()

def updateMoves(move_id, name, move_type, power, accuracy, pp, class_type):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO moves (id, name, type, power, accuracy, pp, class_type) VALUES (?, ?, ?, ?, ?, ?, ?)", (move_id, name, move_type, power, accuracy, pp, class_type))
    db.commit()
    db.close()

def updateTypes(type, doubledmgfrom, doubledmgto, halfdmgfrom, halfdmgto, nodmgfrom,nodmgto):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO types (type, double_dmg_from, double_dmg_to, half_dmg_from, half_dmg_to, no_dmg_from, no_dmg_to) VALUES (?, ?, ?, ?, ?, ?, ?)", (type, doubledmgfrom, doubledmgto, halfdmgfrom, halfdmgto, nodmgfrom, nodmgto))
    db.commit()
    db.close()

def updatePokeMove(pokemon_name, move_id):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO pokemon_moves (poke_name, move_id) VALUES (?, ?)", (pokemon_name, move_id))
    db.commit()
    db.close()

def updateGameHistory(game_number, winner, loser, current_time):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    #winnerID = getUserID(winner)
    #loserID = getUserID(loser)
    c.execute("INSERT INTO gameHistory (game_ID, winner, loser, time_completed) VALUES (?, ?, ?, ?)", (game_number, winner, loser, current_time))
    db.commit()
    db.close()

def updateGamePokeList(game_ID, user, poke_name,active_hp, active_status, move1, move2, move3, move4):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO gamePokeStats (game_ID, user, poke_name, active_hp, active_status, move1, move2, move3, move4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (game_ID, user, poke_name, active_hp, active_status, move1, move2, move3, move4))
    db.commit()
    db.close()

def updateChallengeInitial(user1, user2):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO gameChallenge (accepted_status, challenger, challenged) VALUES (?,?, ?)", ("None",user1,user2))
    db.commit()
    db.close()

def updateChallengeFinal(accepted_status, challenger, challenged):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE gameChallenge SET accepted_status = ? WHERE challenger = ? AND challenged = ?", (accepted_status, challenger, challenged))
    db.commit()
    db.close()

# Database Manipulation

#Selecting specific argument-based data
def getTableData(table, valueType, value):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # make sure that this all exists
    c.execute("SELECT * FROM " + table + " WHERE " + valueType + " = ?", (value,))
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1

def getPokeData(table, valueType, value):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # make sure that this all exists
    c.execute("SELECT * FROM " + table + " WHERE " + valueType + " LIKE ?", (value,))
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1

def getChallengeData(accepted_status, challenger, challenged):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM gameChallenge WHERE accepted_status = ? AND challenger = ? AND challenged = ?", (accepted_status, challenger, challenged))
    result = c.fetchall()
    db.close()
    if result:
        return result
    else:
        return -1

def getChallengeHistory(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM gameChallenge WHERE challenger = ? OR challenged = ?", (username, username))
    result = c.fetchall()
    db.close()
    if result:
        return result
    else:
        return -1

def deleteChallenge(challenger, challenged):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DELETE FROM gameChallenge WHERE challenge_ID = (SELECT MAX(challenge_ID) FROM gameChallenge) AND challenger = ? AND challenged = ?", (challenger, challenged))
    db.commit()
    db.close()

#Selecting specific argument-based data -- same as getTableData except gets all rows instead of only one
def getAllTableData(table, valueType, value):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # make sure that this all exists
    c.execute("SELECT * FROM " + table + " WHERE " + valueType + " = ?", (value,))
    result = c.fetchall()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1

def getStatFilteredData(table, stat, operator, value):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    query = f"SELECT * FROM pokeDex WHERE {stat} {operator} ?"
    c.execute(query, (value,))
    pokemon_data = c.fetchall()
    db.close()
    return pokemon_data

#Updates a value in a table with a new value
def setTableData(table, updateValueType, newValue, valueType, value):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute(f"UPDATE {table} SET {updateValueType} = '{newValue}' WHERE {valueType} = ?", (value,))
    db.commit()
    db.close()

#Updates a value in a table with a new value
def setActiveHP(new_HP, game_id, username, pokename):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute(f"UPDATE gamePokeStats SET active_hp = '{new_HP}' WHERE game_ID = ? AND user = ? AND poke_name = ?", (game_id,username,pokename))
    db.commit()
    db.close()

#Selected all user-specific matches
def getGameHistory(userID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM gameHistory WHERE winner = ? OR loser = ?", (userID, userID))
    result = c.fetchall()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1

#Select latest game played based on ID
def getLatestGameHistory():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM gamePokeStats ORDER BY game_ID DESC",)
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1
#Select latest game challenge based on ID
def getLatestChallenge():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * FROM gameChallenge ORDER BY challenge_ID DESC",)
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1



#Returning all data in any table
def getTable(tableName):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * from " + tableName)
    a = c.fetchall()
    db.close()
    return a

def resetChallenge():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE gameChallenge SET accepted_status = ?", ("Over",))
    c.execute("UPDATE users SET in_game = ?", ("No",))
    db.commit()
    db.close()

#Resetting any table
def resetTable(tableName):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DELETE FROM " + tableName)
    db.commit()
    db.close()
