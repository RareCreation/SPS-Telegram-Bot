import asyncio

from handlers.bot_instance import dp, bot
from utils.console.logger_util import logger
from utils.setup_commands.setup_bot_commands_util import setup_bot_commands
from utils.telegram.routers.load_routers_util import load_routers

activated_receipt = set()


async def main():
    logger.info("Initializing database...")

    logger.info("Bot has been loaded")
    # await setup_bot_commands(bot)

    await load_routers(dp=dp, bot=bot)
    logger.info("routers loaded")

    logger.info("Starting bot polling...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logger.info("Launching bot application...")

    asyncio.run(main())
