import json
from pathlib import Path


def obtener_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

def guarda_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
    
        json.dump(config, f, indent=4, ensure_ascii=False)


def existe_config():

    config = Path("config.json")

    # En caso que no exista el archivo
    if not config.exists():
        return False
    
    return True

