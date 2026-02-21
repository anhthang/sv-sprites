import os
import requests
import re

SPRITE_FOLDER = "sprites"

# Caching for both species and specific pokemon data
species_cache = {}
pokemon_cache = {}


def get_data(url, cache):
    """Generic cached getter."""
    if url in cache:
        return cache[url]

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cache[url] = data
        return data
    return None


def get_variety_name(dex_id, index):
    """
    Logic:
    1. Try species varieties first.
    2. If index is out of range, check the default pokemon's 'forms' list.
    """
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{dex_id}"
    species_data = get_data(species_url, species_cache)

    if not species_data:
        return f"unknown-{dex_id}"

    species_name = species_data["name"]
    varieties = species_data.get("varieties", [])

    # Rule 1: Check Varieties
    if index < len(varieties):
        full_name = varieties[index]["pokemon"]["name"]
        suffix = full_name.replace(species_name, "").strip("-")
        return suffix if suffix else "base"

    # Rule 2: Check Forms of the default variety
    # Get the URL for the first (default) variety to find its forms
    if varieties:
        default_pokemon_url = varieties[0]["pokemon"]["url"]
        pokemon_data = get_data(default_pokemon_url, pokemon_cache)

        if pokemon_data:
            forms = pokemon_data.get("forms", [])
            if index < len(forms):
                form_name = forms[index]["name"]
                suffix = form_name.replace(species_name, "").strip("-")
                return suffix

    # Fallback if index is still not found
    return f"form-{index}"


def process_files():
    if not os.path.exists(SPRITE_FOLDER):
        print(f"Folder {SPRITE_FOLDER} not found.")
        return

    files = sorted([f for f in os.listdir(SPRITE_FOLDER) if f.endswith(".png")])

    for filename in files:
        match = re.match(r"(\d+)(?:_(\d+))?\.png", filename)
        if not match:
            continue

        raw_id, raw_index = match.groups()
        dex_id = int(raw_id)
        variety_idx = int(raw_index) if raw_index else 0

        # Simple case: 0001.png -> 1.png
        if variety_idx == 0:
            new_name = f"{dex_id}.png"
        else:
            # Complex case: variety/form lookup
            suffix = get_variety_name(dex_id, variety_idx)
            new_name = f"{dex_id}-{suffix}.png"

        old_path = os.path.join(SPRITE_FOLDER, filename)
        new_path = os.path.join(SPRITE_FOLDER, new_name)

        try:
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")


if __name__ == "__main__":
    process_files()
