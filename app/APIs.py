# ChewyChupucabras - Tanzeem Hasan, Ethan Sie, Brian Liu
# SoftDev
# P02:
# 2024-01-XX
# Time Spent: not enough hours

from flask import Flask, request, jsonify, render_template
import urllib.parse
import urllib.request
import requests
import json
import db

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from {url}: {response.status_code}")
        return None

def fetch_moves():
    moves_url = "https://pokeapi.co/api/v2/move?limit=1000"
    moves_data = fetch_data(moves_url)

    if moves_data:
        for move in moves_data['results']:
            move_details = fetch_data(move['url'])
            if move_details and move_details['generation']['name'] == 'generation-i':
                # Extract move details
                move_id = move_details['id']
                name = move_details['name']
                move_type = move_details['type']['name']
                power = move_details['power'] if move_details['power'] else None
                accuracy = move_details['accuracy'] if move_details['accuracy'] else None
                pp = move_details['pp']
                class_type = move_details['damage_class']['name'] if move_details['damage_class']['name'] else None
                # Insert move into the database
                db.updateMoves(move_id, name, move_type, power, accuracy, pp, class_type)

                # Fetch Pokémon that can learn the move
                for learn_method in move_details['learned_by_pokemon']:
                    pokemon_name = learn_method['name']
                    db.updatePokeMove(pokemon_name, move_id)

def fetch_poke():
    pokemon_url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    pokemon_data = fetch_data(pokemon_url)

    if pokemon_data:
        for pokemon in pokemon_data['results']:
            pokemon_details = fetch_data(pokemon['url'])
            if pokemon_details:
                name = pokemon_details['name']
                types = pokemon_details['types']
                type_1 = types[0]['type']['name'] if len(types) > 0 else None
                type_2 = types[1]['type']['name'] if len(types) > 1 else None

                stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_details['stats']}
                hp = stats.get('hp', None)
                attack = stats.get('attack', None)
                defense = stats.get('defense', None)
                special_attack = stats.get('special-attack', None)
                special_defense = stats.get('special-defense', None)
                speed = stats.get('speed', None)
                sprite_url = pokemon_details['sprites']['front_default']
                # Insert Pokémon into the database
                db.updatePokeList(name, type_1, type_2, hp, attack, defense, special_attack, special_defense, speed, sprite_url)
