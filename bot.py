import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import AllowedUpdates

from filters.moder_group import IsModerGroup
from handlers.check import register_check_queue
from handlers.get_granted import register_get_granted
from handlers.restore import register_restore
from tgbot.handlers.grant_cancel_callback import register_cancel_grant
from tgbot.handlers.grant_callback import register_grant
from tgbot.filters.granted import IsNotGranted
from tgbot.filters.count import IsGrantCount
from tgbot.filters.user_group import IsUserGroup
from tgbot.Utils.DBWorker import create_tables
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.group_join import IsGroupJoin
from tgbot.handlers.admin import register_admin
from tgbot.handlers.catch_update import register_catch
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(LoggingMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroupJoin)
    dp.filters_factory.bind(IsUserGroup)
    dp.filters_factory.bind(IsModerGroup)
    dp.filters_factory.bind(IsGrantCount)
    dp.filters_factory.bind(IsNotGranted)


def register_all_handlers(dp):
    # register_echo(dp)
    register_admin(dp)
    register_user(dp)
    register_catch(dp)
    register_grant(dp)
    register_cancel_grant(dp)
    register_check_queue(dp)
    register_restore(dp)
    register_get_granted(dp)



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await create_tables()

    # start
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.CHAT_MEMBER + AllowedUpdates.CALLBACK_QUERY)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")