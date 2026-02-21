# Pokémon SV-Style HOME Sprites

This repository is a curated collection of Pokémon sprites in the **Scarlet & Violet (SV) style**.

## 🎯 Purpose

The goal of this project is to bring the modern, high-fidelity "HOME" sprite aesthetic to the **[Raycast Pokédex Extension]**.

Currently, many PokéAPI-linked resources are missing these specific assets or rely on older generation artwork. I wanted a more consistent and "cool" look for my Pokédex, so I’ve aggregated and renamed these to be developer-friendly. Once the collection is fully stabilized, I plan to submit a **Pull Request** to the original extension or PokéAPI contributors to make this style available for everyone.

## 🛠 Naming Convention

A key feature of this repo is the **Standardized Form Naming**.

By default, PokéAPI assigns varieties and cosmetic forms IDs starting at `10000` (e.g., Mega Charizard X is `10034`). To make asset management more intuitive for developers, this repo uses a **Base-Dex-ID + Suffix** format.

### The Logic

1. **Base Pokémon**: Uses the simple Dex number.

    * `1.png` (Bulbasaur)
    * `25.png` (Pikachu)

2. **Varieties & Forms**: Uses the format `{dex_number}-{form_name}.png`.

    * The `form_name` is derived from the PokéAPI `pokemon.name` field, with the base species name removed.
    * **Varieties**: `6-mega-x.png` (instead of `10034.png`)
    * **Cosmetic Forms**: `666-polar.png` (instead of `666_01.png`)

### Examples

| Pokémon | Source Name | Repo Filename |
| --- | --- | --- |
| Bulbasaur | `0001.png` | `1.png` |
| Mega Charizard X | `0006_01.png` | `6-mega-x.png` |
| Alolan Raichu | `0026_01.png` | `26-alola.png` |
| Vivillon (Polar) | `0666_01.png` | `666-polar.png` |

## 📥 How to Sync

If you are contributing or updating the assets, the included scripts handle the heavy lifting:

1. **`download_sprites.py`**: Scrapes the latest assets from Project Pokémon.
2. **`rename_sprites.py`**: Queries PokéAPI to translate numeric indices into readable form names.

## ⚠️ Important Note on Naming Accuracy

While the automated script handles standard forms (Mega, Alola, Galar, Hisui, etc.) reliably, users and contributors should **double-check** Pokémon with high-count varieties:

* **Pikachu**: Cosplay and Hat variants.
* **Vivillon**: The 20+ patterns.
* **Alcremie**: The various sweets/cream combinations.
* **Minior**: Core colors.

> [!WARNING]
> **Index Mismatch:** Project Pokémon's file indexing (e.g., `_01`, `_02`) does not always match the array order in PokéAPI's `varieties` or `forms` endpoints. Please manually verify these "multi-form" Pokémon before using them in a production environment.

## 📜 Credits

* **Sprites**: Sourced from [Project Pokémon].
* **Data**: Powered by [PokéAPI](https://pokeapi.co/).

[Project Pokémon]: https://projectpokemon.org/home/docs/spriteindex_148/switch-sv-style-sprites-for-home-r153/
[Raycast Pokédex Extension]: https://www.raycast.com/anhthang/pokedex
