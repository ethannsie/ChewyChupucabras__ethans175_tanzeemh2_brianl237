# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Brian Liu
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
    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, created_at TEXT, last_login TEXT);")
    # Database holds all of the pokemon information for gen1
    c.execute("CREATE TABLE IF NOT EXISTS pokeDex (history_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, search_type TEXT, location_name TEXT, search_time TEXT);")
    # Database keeps track of any six collection of pokemons from each game
    c.execute("CREATE TABLE IF NOT EXISTS gamePokeSets (game_ID INTEGER PRIMARY KEY, user TEXT, poke1 TEXT, poke2 TEXT, poke3 TEXT, poke4 TEXT, poke5 TEXT, poke6 TEXT);")
    c.execute("CREATE TABLE IF NOT EXISTS gameHistory (game_ID INTEGER PRIMARY KEY AUTOINCREMENT, winner TEXT, loser TEXT, time_completed TEXT);")
    db.commit()
    db.close()

def addUser(username, password):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # datetime formatting for sqlite text
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # omits userID as an input as it autoincrements
    c.execute("INSERT INTO users (username, password, created_at, last_login) VALUES (?, ?, ?, ?)", (username, password, created_at, created_at))
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

def updateGameHistory(game_number, winner, loser, current_time):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    winnerID = getUserID(winner)
    loserID = getUserID(loser)
    c.execute("INSERT INTO userHistory (game_ID, winner, loser, time_completed) VALUES (?, ?, ?, ?)", (game_number, winnerID, loserID, current_time))
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
        return None

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
        return None

#Returning all data in any table
def getTable(tableName):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT * from " + tableName)
    a = c.fetchall()
    db.close()
    return a

#Resetting any table
def resetTable(tableName):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DELETE FROM " + tableName)
    db.commit()
    db.close()
