# ChewyChupucabras - Tanzeem Hasan, Ethan Sie, Brian Liu
# SoftDev
# P02:
# 2024-01-XX
# Time Spent: not enough hours

import db
import random

#recieves username of players (could be changed to challengeID); gives them 6 random pokemon with 4 random moves
def startgame(player1, player2):
    id = 1 if db.getLatestGameHistory() == -1 else db.getLatestGameHistory()[0] + 1
    for player in [player1, player2]:
        #slightly messy but gets a random move_id from pokemon_moves table four times for each of the six pokemon. data is then stored in gamePokeStats
        #possible issue is that there are duplicate moves/pokemon selected
        randomPoke = db.getTable("pokeDex")[random.randint(0, len(db.getTable("pokeDex")) - 1)][1]
        move1_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
        move2_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
        move3_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
        move4_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
        db.updateGamePokeList(id, player, randomPoke, db.getTableData("pokeDex", "poke_name", randomPoke)[4], "True", move1_ID, move2_ID, move3_ID, move4_ID)

        for i in range(5): 
            randomPoke = db.getTable("pokeDex")[random.randint(0, len(db.getTable("pokeDex")) - 1)][1]
            move1_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
            move2_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
            move3_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
            move4_ID = db.getAllTableData("pokemon_moves", "poke_name", randomPoke)[random.randint(0, len(db.getAllTableData("pokemon_moves", "poke_name", randomPoke)) - 1)][1]
            
            db.updateGamePokeList(id, player, randomPoke, db.getTableData("pokeDex", "poke_name", randomPoke)[4], "False", move1_ID, move2_ID, move3_ID, move4_ID)

#js needs the toggle corresponding active_statuses in gamePokeStats 
def swapPokemon(swapPokeName):
    #for loop searches for gamePokeStats rows with a certain gameID and username until it finds the pokemon with active_status set to True
    #once found, toggles it to False and switchs the corresponding row with swapPokeName to True
    return

def turn():
    return

def battletext():
    return ["Player 1's Diglett used earthquake! It did x damage!", "Player 2's Pikachu used "]

#recieves name of move used, name of attacking pokemon, name of recieving pokemon; returns dmg
def damageCalc(move, attacker, reciever):
    #Base Stats + RNG
    pokeLevel = 100 #probably standardized?
    crtical = 2 if (random.randint(0, 255) > random.randint(0, 255)) else 1
    movePower = db.getTableData("moves", "name", move)[3]
    rng = (random.randint(217, 255)) / 255
    #ATK + DEF Stats
    if (db.getTableData("moves", "name", move)[6] == 'physical'):
        attackerATK = db.getTableData("pokeDex", "poke_name", attacker)[5]
        recieverDEF = db.getTableData("pokeDex", "poke_name", reciever)[6]
    else:
        attackerATK = db.getTableData("pokeDex", "poke_name", attacker)[7]
        recieverDEF = db.getTableData("pokeDex", "poke_name", reciever)[8]
    #Same Attack Type Bonus
    stab = 1.5 if db.getTableData("moves", "name", move)[2] == db.getTableData("pokeDex", "poke_name", attacker)[2] or db.getTableData("moves", "name", move)[2] == db.getTableData("pokeDex", "poke_name", attacker)[3] else 1
    #Type Matchup Multipliers
    movetype = db.getTableData("moves", "name", move)[2]
    typeMultipler = 1
    for recievertype in [db.getTableData("pokeDex", "poke_name", reciever)[2], db.getTableData("pokeDex", "poke_name", reciever)[3]]:
        if recievertype:
            if (recievertype in db.getTableData("types", "type", movetype)[3]):
                typeMultipler *= 2
            if (recievertype in db.getTableData("types", "type", movetype)[5]):
                typeMultipler *= 0.5
            if (recievertype in db.getTableData("types", "type", movetype)[7]):
                typeMultipler *= 0
    #print(f"level: {pokeLevel}, crit: {crtical}, power: {movePower}")
    #print(f"atk: {attackerATK}, def: {recieverDEF}, stab: {stab}, rng: {rng}")
    #print(f"typeMulti: {typeMultipler}")

    return (((((((2.0 * pokeLevel * crtical) / 5) + 2) * movePower * attackerATK / recieverDEF) / 50) + 2) * stab * typeMultipler * rng)

#recieves id of the game; updates players' elo based on winner/loser
def updateElo(gameID):
    winner_user = db.getTableData("gameHistory", "game_ID", gameID)[1]
    loser_user = db.getTableData("gameHistory", "game_ID", gameID)[2]
    
    pokemonAlive = 0
    match_pokemon = (db.getAllTableData("gamePokeStats", "game_ID", gameID)) # gets data of all the pokemon in the match from gamePokeStats
    for pokemon_data in match_pokemon:
        print(pokemon_data)
        if pokemon_data[1] == winner_user and pokemon_data[3] > 0:
            pokemonAlive += 1
    
    winner_elo = db.getTableData("users", "username", winner_user)[3] + 10 + (pokemonAlive * 5)
    loser_elo = db.getTableData("users", "username", loser_user)[3] - 20

    db.setTableData("users", "rank", winner_elo, "username", winner_user)
    db.setTableData("users", "rank", loser_elo, "username", loser_user)

