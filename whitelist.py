import json
import yaml
import requests

MOJANG_API_URL = "https://api.mojang.com/users/profiles/minecraft/{}"
INPUT = "whitelist.yaml"
OUTPUT = "whitelist.json"

def get_uuid(playername):
    response = requests.get(MOJANG_API_URL.format(playername))
    if response.status_code == 200:
        return response.json()['id']
    return None

def load_and_sort_yaml(yaml_path) -> list[str]:

    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        entries = data.get('whitelist', [])

    # Doppelte Einträge entfernen und Liste alphabetisch sortieren
    playernames = sorted(set(entries))

    # Sortierte und bereinigte Liste wieder in das ursprüngliche Format umwandeln
    data['whitelist'] = playernames

    # Die bereinigte und sortierte Liste in der YAML-Datei speichern
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    return playernames

# Funktion zur Erstellung der Whitelist
def create_whitelist(player_names, existing_whitelist='whitelist.json'):
    try:
        with open(existing_whitelist, 'r') as file:
            whitelist = json.load(file)
    except FileNotFoundError:
        whitelist = []

    # Erstelle ein Set von vorhandenen UUIDs für eine schnelle Überprüfung
    existing_uuids = {entry['uuid'] for entry in whitelist}

    for player_name in player_names:
        player_uuid = get_uuid(player_name)
        if player_uuid:
            if player_uuid not in existing_uuids:
                # Spieler zur Whitelist hinzufügen
                new_entry = {
                    "uuid": player_uuid,
                    "name": player_name
                }
                whitelist.append(new_entry)
                existing_uuids.add(player_uuid)  # UUID zum Set hinzufügen
                print(f"Hinzugefügt: {player_name} (UUID: {player_uuid})")
            else:
                print(f"Spieler mit UUID {player_uuid} (Name: {player_name}) ist bereits vorhanden.")
        else:
            print(f"Nicht gefunden: {player_name}")

    # Whitelist in Datei speichern
    with open(existing_whitelist, 'w') as file:
        json.dump(whitelist, file, indent=4)
    print("Whitelist erfolgreich aktualisiert.")


# Hauptprogramm
def main(yaml_path='whitelist.yaml', whitelist_path='whitelist.json'):
    # Spieler aus YAML laden und sortieren
    player_names = load_and_sort_yaml(yaml_path)

    # Whitelist erstellen oder aktualisieren
    create_whitelist(player_names, whitelist_path)

# Beispielaufruf des Hauptprogramms
if __name__ == "__main__":
    main()
