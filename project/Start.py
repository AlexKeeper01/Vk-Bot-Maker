from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import sqlite3

f = open("tock_en.txt", encoding="cp1251")
lines = f.read()

di = dict()                #Создаём словарь(так надо)
con = sqlite3.connect("com.db")
cur = con.cursor()
x = cur.execute(f"""SELECT * FROM commands""").fetchall()
for q in x:
    di[q[0]] = q[1]


#Ну в принципе дальше идёт то, в чём здоровый на голову человек даже не будет пытаться разобраться(я уверяю, там всё норм)
vk_session = vk_api.VkApi(token=lines)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.from_user and not (event.from_me):
            print('Текст сообщения: ' + str(event.text))
            print(event.user_id)
            y = di.get(event.text)
            if y != None:
                vk_session.method('messages.send', {'user_id': event.user_id, 'message': y, 'random_id': 0})