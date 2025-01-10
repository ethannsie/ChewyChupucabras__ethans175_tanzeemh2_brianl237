# ChewyChupucabras - Tanzeem Hasan, Ethan Sie, Brian Liu
# SoftDev
# P02:
# 2024-01-XX
# Time Spent: not enough hours

import db
import random

def startgame():
    return

def turn():
    return

def battletext():
    return

#Returns damage
#recieves name of move used, name of attacking pokemon, name of recieving pokemon
def damageCalc(move, attacker, reciever):
    pokeLevel = 100 #probably standardized?
    crtical = 2 if (random.randint(0, 255) > random.randint(0, 255)) else 1
    movePower = db.getTableData("moves", "name", move)[3]
    if (db.getTableData("moves", "name", move)[6] == 'physical'):
        attackerATK = db.getTableData("pokeDex", "poke_name", attacker)[5]
        recieverDEF = db.getTableData("pokeDex", "poke_name", reciever)[6]
    else:
        attackerATK = db.getTableData("pokeDex", "poke_name", attacker)[7]
        recieverDEF = db.getTableData("pokeDex", "poke_name", reciever)[8]
    stab = 1.5 if db.getTableData("moves", "name", move)[2] == db.getTableData("pokeDex", "poke_name", attacker)[2] or db.getTableData("moves", "name", move)[2] == db.getTableData("pokeDex", "poke_name", attacker)[3] else 1
    ###not sure how this will be implemented yet
    #ok this is far from optimized
    movetype = db.getTableData("moves", "name", move)[2]
    for recievertype in [db.getTableData("pokeDex", "poke_name", reciever)[2], db.getTableData("pokeDex", "poke_name", reciever)[3]]:
        weakagainst = db.getTableData("types", "type", i)[2]
        resistantagainst = db.getTableData("types", "type", i)[4]
        immuneagainst = db.getTableData("types", "type", i)[6]
        for matchups in weakagainst
            if (movetype == )

    type1 = 0
    type2 = 0
    print(type_matchup)

    rng = (random.randint(217, 255)) / 255
    #print(f"level: {pokeLevel}, crit: {crtical}, power: {movePower}")
    #print(f"atk: {attackerATK}, def: {recieverDEF}, stab: {stab}, rng: {rng}")

    return (((((((2.0 * pokeLevel * crtical) / 5) + 2) * movePower * attackerATK / recieverDEF) / 50) + 2) * stab * type1 * type2 * rng)

damageCalc("earthquake","diglett","pikachu")
