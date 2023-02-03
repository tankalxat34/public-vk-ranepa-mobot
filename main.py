# Модули для общего использования во всех файлах бота
from vk_api.longpoll import VkEventType
from vk_api import VkUpload  # для загрузки картинок на сервер вк
import const
from botlib import schedule
import re


# Модули для локального использования только в этом файле
import time
import core
import traceback
import json


def main():
    """Точка входа в программу"""
    # ИНИЦИАЛИЗАЦИЯ ЛОКАЛЬНЫХ ПЕРЕМЕННЫХ
    local_choice = {}
    wait_links = {}

    for event in longpoll.listen():
        # print(event.type)
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            text = event.text.lower()
            user_id = event.user_id

            ### ПЕРСОНАЛИЗАЦИЯ ЛОКАЛЬНЫХ ПЕРЕМЕННЫХ ПОД КОНКРЕТНОГО ПОЛЬЗОВАТЕЛЯ ###
            local_choice[str(user_id)] = {}
            
            if text == "начать" or text == "в главное меню":
                core.send(user_id, 
f"""Привет, {core.vkname(user_id)}! Это неофициальный чат-бот @moranepa (Московского областного филиала РАНХиГС), разрабатывающийся студентом филиала @tankalxat34 (Александром Подстречным).
            
Выбери на клавиатуре ниже одну из доступных функций бота!""", keyboard=const.BotKeyboards.main())

            ### РАСПИСАНИЕ ###
            elif text == "узнать расписание":
                core.firstSendSchedule(user_id)

            elif text in schedule.DIRECTIONS_LIST:
                local_choice[str(user_id)]["direction"] = text
                core.send(user_id, "На каком курсе вы обучаетесь?", const.BotKeyboards.choiceKurs())
            
            elif text in schedule.KURS:
                local_choice[str(user_id)]["kurs"] = int(text)
                core.send(user_id, "Какая ваша форма обучения?", const.BotKeyboards.choiceOz())

            elif text in schedule.OZ:
                local_choice[str(user_id)]["oz"] = (text != schedule.OZ[0])
                core.send(user_id, "Ваша форма высшего образования?", const.BotKeyboards.choiceMag())

            elif text in schedule.MAG:
                local_choice[str(user_id)]["mag"] = (text != schedule.MAG[0])
                core.sendSchedule(user_id, local_choice)
                core.send(user_id, "Вы можете сохранить выбор расписания. Это позволит в дальнейшем не выбирать множество критериев и мгновенно получать расписание по нажатию кнопки", const.BotKeyboards.choiceSave())

            elif text == "сохранить расписание":
                const.USERS_CHOICE[str(user_id)] = local_choice[str(user_id)]
                const.USERS_CHOICE_FILE.commit(json.dumps(const.USERS_CHOICE), f"{core.vkname(user_id, 'full')} ({user_id}) → сохранено расписание")
                core.send(user_id, "Расписание успешно сохранено!", const.BotKeyboards.main())

            elif text == "сообщить об ошибке":
                try:
                    core.send(int(const.CONST["bigBoss"]), f"❤ У пользователя @id{user_id} ({core.vkname(user_id, 'full')}) произошла ошибка в получении расписания:\n" + json.dumps(local_choice[str(user_id)], indent=2))
                except Exception:
                    core.send(int(const.CONST["bigBoss"]), f"❤ У пользователя @id{user_id} ({core.vkname(user_id, 'full')}) произошла ошибка в получении расписания!")
                core.send(user_id, "Спасибо, репорт отправлен!", const.BotKeyboards.main())

            elif text == "сбросить":
                core.killChoice(user_id)               

            ### ГЕНЕРАТОР БИБЛИОГРАФИЧЕСКИХ ССЫЛОК ###
            elif text == "создать список литературы":
                core.send(user_id, "Отправьте мне ссылку или ссылки на электронные ресурсы (ссылки должны быть в одном сообщении), которыми вы пользовались при написании курсовой/дипломной/научной или любой другой работы, требующей оформления по ГОСТу.\n\nВ ответ бот вышлет библиографические ссылки для списка литературы в вашей работе", const.BotKeyboards.backToMainMenu())

            elif re.findall(const.REGEXP["url"], text):
                core.createLinksString(user_id, text)

            ### ОБРАБОТКА ПОДПИСОК НА ГРУППУ ###

            ### ОБЩИЙ ФУНКЦИОНАЛ ###
            elif text == "/обновить":
                core.updateBot(user_id)
            
            else:
                core.send(user_id, "К сожалению я не понял вашей команды")


if __name__ == "__main__":
    while True:
        try:
            vk = const.VK
            longpoll = const.LONGPOLL
            upload = const.UPLOAD
            print(time.strftime("%H:%M:%S"), ":: Bot has been started")
            main()
        except Exception:
            print(traceback.format_exc())
