from aiogram import md
from aiogram import types


async def get_link(user: types.User):
    if not user.url:
        return 'пользователь'
    if user.first_name:
        username = user.first_name
        if user.last_name:
            username += f' {user.last_name}'
    elif user.username:
        username = user.username
    else:
        username = 'пользователь'
    return md.hlink(username, user.url)