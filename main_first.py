import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from token import tok
from threading import Thread

vk_session = vk_api.VkApi(token=tok)
longpoll = VkBotLongPoll(vk_session, 188446752)


class User:
    def __init__(self, id, clan, clas):
        self.clan = clan
        self.id = id
        self.life = True
        self.clas = ''


class Clan:
    def __init__(self, name, chat):
        self.name = name
        self.chat = chat
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def delete_user(self, id):
        for i in range(len(self.users)):
            if self.users[i].id == id:
                del self.users[i]


users = []
clans = []


def sender(id, text):
    vk_session.method('messages.send', {'random_id': 0, 'chat_id': id, 'message': text})


def info(id):
    try:
        sexs = {1: 'Женский', 2: 'Мужской'}
        ans = f'Информация о пользователе @id{id}'
        data = vk_session.method('users.get', {"user_id": id, "name_case": "Nom", "fields": [
            "sex, bdate, city, country, status, followers_count, online"]})[0]
        ans = f"{ans}\nИмя: {data['first_name']}\nФамилия: {data['last_name']}\nПол: {sexs[data['sex']]}\nДата рождения: {data['bdate']}\nСтрана: {data['country']['title']}\nГород: {data['city']['title']}\nСтатус: {data['status']}\nКоличество подписчиков: {data['followers_count']}\n"
        if data['online']:
            ans = f'{ans} пользователь сейчас онлайн'
        else:
            ans = f'{ans} пользователь сейчас не онлайн'
        return ans
    except Exception as e:
        return 'Мы не можем найти информацию о данном пользователе!'


def check_users(id):
    global users
    ans = 0
    for user in users:
        if user.id == id:
            ans = 1
    return ans


def execute(event):
    id = event.chat_id
    user_id = event.object.message['from_id']
    msg = event.object.message['text'].lower()

    if id == 27:

        if not (check_users(user_id)):
            users.append(User(user_id, '', ''))
            sender(id,
                   f'Приветствую тебя, @id{user_id}!\nЧтобы вступить в клан, введи "Кланы"\nЧтобы выбрать класс персонажа, введи "Классы"')

        for user in users:
            if user.id == user_id:

                if msg == 'классы':
                    if user.clas == '':
                        sender(id,
                               'Вот доступные классы:\n1) Маги\n2) Войны\nЧтобы выбрать класс, введи "Выбрать + название класса"\nУдачи тебе!')
                    else:
                        sender(id,
                               f'@id{user_id}, у тебя уже есть класс, это класс {user.clas}\nКласс персонажа менять нельзя!')

                if msg == 'кланы':
                    string = 'Доступные кланы:\n\n'
                    for clan in clans:
                        if clan.chat == id:
                            string = f'{string}{clan.name}\n'
                    sender(id, string)

                if ((msg.startswith('выбрать')) and (msg.split()[1] in ['маги', 'войны'])):
                    if user.clas == '':
                        if msg == 'выбрать маги':
                            user.clas = 'маги'
                        elif msg == 'выбрать войны':
                            user.clas = 'войны'
                        sender(id, f'Поздравляем, вы выбрали класс {user.clas}')
                    else:
                        sender(id,
                               f'@id{user_id}, у тебя уже есть класс, это класс {user.clas}\nКласс персонажа менять нельзя!')

                if ((msg.startswith('создать клан')) and (msg.replace('создать клан', '', 1).strip())):
                    if user.clan == '':
                        flag = 1
                        for clan in clans:
                            if (clan.name == msg.replace('создать клан', '', 1)) and (clan.chat == id):
                                flag == 0
                        print(flag)
                        if flag:
                            if user.clan == '':
                                clans.append(Clan(msg.replace('создать клан', '', 1).strip(), id))
                                print(clans)
                                for i in range(len(clans)):
                                    if ((clans[i].name == msg.replace('создать клан', '', 1).strip()) and (
                                            clans[i].chat == id)):
                                        clans[i].add_user(user)
                                        user.clan = msg.replace('создать клан', '', 1).strip()
                                        sender(id,
                                               f"Поздравляем, вы успешно создали клан {msg.replace('создать клан', '', 1).strip()}")
                        else:
                            sender(id, "Такой клан уже существует в этом чате!\nВыберите другое название")
                    else:
                        sender(id, f'У вас уже есть клан!\nЭто клан {user.clan}')

                if msg == 'выйти из клана':
                    if user.clan != '':
                        for clan in clans:
                            if ((clan.name == user.clan) and (clan.chat == id)):
                                clan.delete_user(user.id)
                                sender(id, f'Вы успешно вышли из клана {user.clan}')
                                user.clan = ''
                    else:
                        sender(id, f"@id{user_id} у вас нет клана!")

                if ((msg.startswith('вступить в клан')) and (msg.replace('вступить в клан', '', 1).strip())):
                    if user.clan == '':
                        for clan in clans:
                            if ((clan.chat == id) and (clan.name == msg.replace('вступить в клан', '', 1).strip())):
                                clan.add_user(user)
                                user.clan = clan.name
                                sender(id, f'Вы успешно вступили в клан {user.clan}')
                    else:
                        sender(id, f'У вас уже есть клан, это клан {user.clan}')

                if msg.startswith('инфо '):
                    if user.life:
                        if user.clas == 'маги':
                            if user.clan:
                                if msg.replace('инфо ', '', 1).isdigit():
                                    flag = 0
                                    for clan in clans:
                                        if clan.name == user.clan:
                                            for man in clan.users:
                                                if man.id == int(msg.replace('инфо ', '', 1)):
                                                    flag = 1
                                                    sender(id, info(man.id))
                                    if flag == 0:
                                        sender(id, 'В вашем клане нет такого пользователя!')
                            else:
                                sender(id,
                                       f'Вы не можете пользоваться данной командой, т.к. не принадлежите ни одному из кланов!')
                        else:
                            sender(id, f'Вы не можете пользоваться данной командой, т.к. не принадлежите классу Магов!')
                    else:
                        sender(id, 'Вы не можете выполнять никаких действий т.к. вы мертвы!')

                if msg.startswith('убить '):
                    if user.life:
                        if user.clas == 'войны':
                            if msg.replace('убить ', '', 1).isdigit():
                                for clan in clans:
                                    for man in clan.users:
                                        if int(msg.replace('убить ', '', 1)) == man.id:
                                            if man.clan != user.clan:
                                                if man.life == True:
                                                    man.life = False
                                                    sender(id,
                                                           f"Вы успешно убили пользователя @id{int(msg.replace('убить ', '', 1))}")
                                                else:
                                                    sender(id, f"Вы не можете убить мёртвого!")
                                            else:
                                                sender(id, "Нельзя убивать игроков своего клана!")
                        else:
                            sender(id,
                                   'Вы не можете убивать игроков, это могут сделать только персонажи класса войнов!')
                    else:
                        sender(id, 'Вы не можете выполнять никаких действий т.к. вы мертвы!')

                if msg.startswith('воскресить '):
                    if user.life:
                        if user.clas == 'маги':
                            if msg.replace('воскресить ', '', 1).isdigit():
                                for clan in clans:
                                    for man in clan.users:
                                        if man.clan == user.clan:
                                            if man.life == False:
                                                man.life = True
                                                sender(id,
                                                       f"Пользователь @id{msg.replace('воскресить ', '', 1)} воскрешён!")
                                            else:
                                                sender(id,
                                                       f"Пользователь @id{msg.replace('воскресить ', '', 1)} не мёртв!")
                        else:
                            sender(id, 'Только персонажи класса Маги могут воскрешать других пользователей!')
                    else:
                        sender(id, 'Вы не можете выполнять никаких действий т.к. вы мертвы!')


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            Thread(target=execute, args=(event,), daemon=True).start()
