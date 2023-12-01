import asyncio
from datetime import datetime, timedelta, timezone
from loguru import logger
from config import settings, app
from database import BaseDAO


async def send_photo(user_id):
    try:
        photo = "https://images.unsplash.com/photo-1602271886918-bafecc837c7a?w=" \
                "800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxz" \
                "ZWFyY2h8Mnx8c29tZXxlbnwwfHwwfHx8MA%3D%3D"
        await app.send_photo(user_id, photo)
        logger.success(f"Photo sent successfully to id {user_id}")
    except Exception as e:
        logger.error(f"Error sending photo to {user_id}: {e}")


async def send_message(user_id, text):
    try:
        await app.send_message(chat_id=user_id, text=text)
        logger.success(f"Message sent successfully to id {user_id}")
    except Exception as e:
        logger.error(f"Error sending message to id {user_id}: {e}")


async def main():
    await app.start()
    while True:
        users = await BaseDAO.find_all()
        for user in users:
            if not user.state == 'finished':
                current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                if (current_time - user.registration_time) > timedelta(minutes=10) and user.state == 'start':
                    await BaseDAO.update(user.user_id, {"state": 'first'})
                    await send_message(user.user_id, 'Добрый день!')
                elif (current_time - user.registration_time) > timedelta(minutes=90) and user.state == 'first':
                    await app.send_message(chat_id=user.user_id, text='Подготовила для вас материал')
                    await send_photo(user.user_id)
                    await BaseDAO.update(user.user_id, {"state": 'second'})
                elif (current_time - user.registration_time) > timedelta(minutes=120) and user.trigger_message:
                    await BaseDAO.update(user.user_id, {"state": 'finished'})
                elif (current_time - user.registration_time) > timedelta(minutes=120) and not user.trigger_message:
                    await app.send_message(chat_id=user.user_id, text='Скоро вернусь с новым материалом!')
                    await BaseDAO.update(user.user_id, {"state": 'finished'})
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
