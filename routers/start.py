import re
import asyncio
from aiogram import Router, Dispatcher
from aiogram.types import Message

from utils.steam.inventory_util import resolve_vanity_url, get_inventory_value, get_steam_profile

router = Router()

def load(dp: Dispatcher) -> None:
    dp.include_router(router)

@router.message()
async def handle_steam_link(message: Message):
    links = re.findall(r"(https?://steamcommunity\.com/(id|profiles)/[a-zA-Z0-9_-]+)", message.text)
    if not links:
        await message.answer("Пожалуйста, отправьте ссылку на профиль Steam.")
        return

    for link, type_ in links:
        try:
            if type_ == "id":
                username = link.split("/id/")[1].split("/")[0]
                steam_id = await asyncio.to_thread(resolve_vanity_url, username)
            else:
                steam_id = link.split("/profiles/")[1].split("/")[0]

            profile = await asyncio.to_thread(get_steam_profile, steam_id)
            inventory = await asyncio.to_thread(get_inventory_value, steam_id)

            text = (
                f"<b>Имя профиля:</b> {profile['profileName']}\n"
                f"<b>SteamID:</b> {steam_id}\n"
                f"<b>Инвентарь:</b> ${inventory['totalValue']:.2f}"
            )

            if profile.get("avatar"):
                await message.answer_photo(photo=profile["avatar"], caption=text, parse_mode="HTML")
            else:
                await message.answer(text, parse_mode="HTML")

        except Exception:
            await message.answer("Данный профиль не удалось обработать. Возможно, он приватный.")
