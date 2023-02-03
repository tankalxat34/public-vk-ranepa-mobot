"""
ФАЙЛ ДЛЯ ФУНКЦИЙ И МЕТОДОВ, КОТОРЫМИ ПОЛЬЗУЕТСЯ БОТ
"""
import json
import sys
import vk_api
import vk_api.keyboard
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload  # для загрузки картинок на сервер вк
import importlib
import const
import random
import traceback
from botlib import schedule, biblio_script
import pyGitConnect
import re


def vkname(user_id, type: str = "first"):
    """Возвращает имя или фамилию написавшего"""
    tmp = const.VK.method('users.get', {'user_ids': user_id})
    if type == 'first' or type == 'last':
        try:
            return tmp[0][type+"_name"]
        except Exception:
            return 'ErrorName'

    elif type == "full":
        try:
            return tmp[0]["first_name"] + " " + tmp[0]["last_name"]
        except Exception:
            return 'ErrorName'


def send(user_id, text, keyboard=None, attachment=None):
    """Отправляет сообщение"""
    return const.VK.method("messages.send",
                           {"user_id": user_id, "message": text, "random_id": random.randint(1, 10 ** 6),
                            "keyboard": keyboard, "attachment": attachment})


class ChoiceDialog(object):
    def direction(user_id):
        send(user_id, "Выберите направление обучения")


def sendSchedule(user_id, user_choice = None):
    if user_choice == None:
        scheduleObject = schedule.ScheduleChecker(
            schedule.DIRECTION_NAME[
                    const.USERS_CHOICE[str(user_id)]["direction"]
                ],
            const.USERS_CHOICE[str(user_id)]["kurs"],
            const.USERS_CHOICE[str(user_id)]["mag"],
            const.USERS_CHOICE[str(user_id)]["oz"])
    else:
        print(user_choice)
        scheduleObject = schedule.ScheduleChecker(
            schedule.DIRECTION_NAME[
                    user_choice[str(user_id)]["direction"]
                ],
            user_choice[str(user_id)]["kurs"],
            user_choice[str(user_id)]["mag"],
            user_choice[str(user_id)]["oz"])
    kbds = scheduleObject.getVkKeyboardsList()
    dates = scheduleObject.getDates()

    print(len(kbds))

    if (len(kbds) != 0):
        for i in range(len(kbds)):
            try:
                send(
                    user_id, f"Расписание на {dates[i]}", keyboard=kbds[i])
            except Exception:
                send(user_id, f"Расписание без даты",
                    keyboard=kbds[i])
    else:
        send(user_id, "Кажется расписания по заданным критериям нет на сайте. Если вы считаете, что произошла ошибка, сообщите об этом, нажав красную кнопку на клавиатуре.\n\nВАЖНО!\nНа данный момент бот может некорректно искать расписание, поскольку на всех сайтах, принадлежащих Академии, введена защита от интернет-запросов, совершаемых не человеком. На данный эта проблема находится на стадии решения, но если вы хотите помочь проекту и ускорить процесс решения, напишите @tankalxat34 (мне в личку)", const.BotKeyboards.sendReport(user_choice))


def firstSendSchedule(user_id):
    try:
        sendSchedule(user_id)
    except Exception:
        send(user_id, "Выберите направление обучения", keyboard=const.BotKeyboards.choiceDirection())


def killChoice(user_id):
    """Сбросить выбор расписания"""
    try:
        del const.USERS_CHOICE[str(user_id)]
        file = pyGitConnect.File(
            const.GITHUB, const.REPOSITORY_NAME + "/content/userChoice.json")
        file.commit(json.dumps(const.USERS_CHOICE),
                    f"({user_id}) - удален выбор")
        send(user_id, "Ваш выбор сброшен", keyboard=const.BotKeyboards.main())
    except KeyError:
        send(user_id, "Выбор не был сброшен, поскольку вы еще ни разу не сохранили расписание",
             keyboard=const.BotKeyboards.main())


def updateBot(user_id):
    if str(user_id) == str(const.CONST["bigBoss"]):
        importlib.reload(const)
        send(user_id, "Бот успешно обновлен!")
    else:
        send(user_id, "У вас нет прав на выполнение этой команды")


def createLinksString(user_id, text):
    local_string = ""
    for url in re.findall(const.REGEXP["url"], text):
        local_string += biblio_script.getLink(url) + "\n\n"

    print(local_string)

    send(user_id, local_string, const.BotKeyboards.main())