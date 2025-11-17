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


def get_steam_profile_webapi(steam_id_or_url: str):
    base_url = "https://www.steamwebapi.com/steam/api/profile"
    params = {
        "id": steam_id_or_url,
        "key": API_KEY,
        "state": "detailed",
        "no_cache": 1,
        "format": "json"
    }
    resp = requests.get(base_url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {
        "steamid": data.get("steamid"),
        "name": data.get("personaname"),
        "avatar": data.get("avatarfull"),
        "profile_url": data.get("profilesteamurl"),
    }

def get_inventory_value(steam_id: str):
    url = "https://www.steamwebapi.com/steam/api/inventory"
    params = {
        "steam_id": steam_id,
        "game": "cs2",
        "key": API_KEY,
        "parse": "true"
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    items = resp.json()
    total_value = sum(float(item.get("pricelatestsell") or 0) for item in items)
    return total_value