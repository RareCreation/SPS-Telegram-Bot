import re

from aiogram import Router, Dispatcher
from aiogram.types import Message

from utils.steam.inventory_util import resolve_vanity_url, get_steam_profile_webapi, get_inventory_value

router = Router()

def load(dp: Dispatcher) -> None:
    dp.include_router(router)


@router.message()
async def handle_steam_link(message: Message):
    links = re.findall(r"(https?://steamcommunity\.com/(id|profiles)/[a-zA-Z0-9_-]+)", message.text)
    if not links:
        await message.answer("Пожалуйста отправьте ссылку")
        return

    for link, type_ in links:
        try:
            if "/id/" in link:
                username = link.split("/id/")[1].strip("/")
                steam_id = resolve_vanity_url(username)
            else:
                steam_id = link.split("/profiles/")[1].strip("/")

            profile = get_steam_profile_webapi(steam_id)
            inventory_value = get_inventory_value(steam_id)

            text = (
                f"<b>Имя профиля:</b> {profile['name']}\n"
                f"<b>SteamID:</b> {profile['steamid']}\n"
                f"<b>Инвентарь:</b>  ${inventory_value:.2f}\n"
            )

            if profile["avatar"]:
                await message.answer_photo(photo=profile["avatar"], caption=text, parse_mode="HTML")
            else:
                await message.answer(text)

        except Exception as e:
            await message.answer(f"Данный профиль не удалось обработать. Возможно он приватный.")
