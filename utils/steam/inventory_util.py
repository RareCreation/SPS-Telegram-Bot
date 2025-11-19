import requests

from config.config import API_KEY, STEAM_API_KEY


def resolve_vanity_url(vanity_url: str) -> str:
    api_url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {"key": STEAM_API_KEY, "vanityurl": vanity_url}
    response = requests.get(api_url, params=params, timeout=10)
    data = response.json()
    if data.get("response", {}).get("success") == 1:
        return data["response"]["steamid"]
    raise ValueError("Кастомный URL не найден или профиль приватный")

def get_steam_profile(steam_id: str) -> dict:

    api_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": STEAM_API_KEY, "steamids": steam_id}
    resp = requests.get(api_url, params=params, timeout=10)
    resp.raise_for_status()
    players = resp.json().get("response", {}).get("players", [])
    if not players:
        raise ValueError("Профиль приватный или не найден")
    player = players[0]
    return {
        "profileName": player.get("personaname", "Unknown"),
        "avatar": player.get("avatarfull")
    }

def get_inventory_value(steam_id: str):
    url = "https://prod-api.lzt.market/steam-value"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "link": f"https://steamcommunity.com/profiles/{steam_id}",
        "app_id": 440,
        "currency": "usd",
        "ignore_cache": True
    }

    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    inventory = data.get("data")
    if not inventory:
        raise ValueError("Инвентарь пустой или профиль приватный")

    return {
        "steam_id": inventory.get("steam_id"),
        "profileName": "Unknown",
        "totalValue": inventory.get("totalValue", 0)
    }
