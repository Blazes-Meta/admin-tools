INPUT = "whitelist.yaml"
OUTPUT = "whitelist.json"

import json
import yaml
import requests

MOJANG_API_URL = "https://api.mojang.com/users/profiles/minecraft/{}"
MOJANG_NAME_API_URL = "https://api.mojang.com/user/profiles/{}/names"

def get_uuid(playername):
    response = requests.get(MOJANG_API_URL.format(playername))
    if response.status_code == 200:
        return response.json()['id']
    return None

def get_name(uuid):
    response = requests.get(MOJANG_NAME_API_URL.format(uuid))
    
    if response.status_code == 200:
        name_history = response.json()
        current_name = name_history[-1]['name']
        return current_name
    else:
        print(f"Kein Spielername für UUID {uuid} gefunden.")
        return None

def load_whitelist(whitelist_path) -> set[str]:
    "Sortiertes Set der UUIDs beliebiger Einträge"
    try:
        with open(whitelist_path, 'r') as file:
            whitelist = json.load(file)
        return sorted({player['uuid'] for player in whitelist})
    except FileNotFoundError: 
        return []

def load_config(yaml_path) -> set[str]:
    "Sortiertes Set der Namen beliebiger Einträge"
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    entrys = data.get('whitelist', [])
    return sorted(set(entrys))


# Funktion zur Erstellung der Whitelist
def create_whitelist(config_file=INPUT,
                     whitelist_file=OUTPUT,
                     existing_whitelist=OUTPUT,
                     respect_whitelist=True):
    
    players_req = load_config(config_file)
    
    if respect_whitelist:
        respected_uuids = load_whitelist(existing_whitelist)
        for uuid in respected_uuids:
            if get_name(uuid):
                players_req.add(get_name(uuid))

    whitelist = []

    for player_name in players_req:
        player_uuid = get_uuid(player_name)
        if player_uuid:
            
            new_entry = {
                "uuid": player_uuid,
                "name": player_name
            }
            whitelist.append(new_entry)
            print(f"Hinzugefügt: {player_name} (UUID: {player_uuid})")
        else:
            print(f"Nicht gefunden: {player_name}")

    # Whitelist in Datei speichern
    with open(whitelist_file, 'w') as file:
        json.dump(whitelist, file, indent=4)
    print("Whitelist erfolgreich aktualisiert.")


create_whitelist(config_file=INPUT,
                 whitelist_file=OUTPUT,
                 existing_whitelist=OUTPUT,
                 respect_whitelist=True)

print(load_config(INPUT))

print(requests.get(MOJANG_NAME_API_URL.format("853c80ef3c3749fdaa49938b674adae6")))