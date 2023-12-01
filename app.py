from pyrogram.handlers import MessageHandler
from config import settings, app
from database import BaseDAO


async def process_messages(client, message):
    from_user_id = message.from_user.id
    text = message.text
    to_user_id = message.chat.id
    existing_user = await BaseDAO.find_one_or_none(user_id=from_user_id)
    if not existing_user:
        await BaseDAO.add(user_id=from_user_id)
    elif from_user_id == to_user_id and text == "/users_today":
        count = await BaseDAO.today_user_count()
        await message.reply(count)
    elif from_user_id == settings.MY_USER_ID and text == "Хорошего дня":
        data = {"trigger_message": True}
        await BaseDAO.update(to_user_id, data)


if __name__ == "__main__":
    handler = MessageHandler(process_messages)
    app.add_handler(handler)
    app.run()
