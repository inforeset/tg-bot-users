from contextlib import suppress

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ChatType
from aiogram.utils.exceptions import MessageToEditNotFound, MessageCantBeDeleted

from Utils.DBWorker import get_data_granted_for_kb
from keyboards.inline import cb
from misc.show_granted import send_granted_message


async def show_granted_cb(call: CallbackQuery, callback_data: dict):
    id_group = callback_data["ids"]
    granted_list = await get_data_granted_for_kb(id_group)
    with suppress(MessageCantBeDeleted, MessageToEditNotFound):
        await call.message.delete()
    await send_granted_message(granted_list, call.message)


def register_show_granted_cb(dp: Dispatcher):
    chat_types = [ChatType.GROUP, ChatType.SUPERGROUP]
    dp.register_callback_query_handler(show_granted_cb, cb.filter(), chat_type=chat_types)