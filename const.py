"""
ФАЙЛ ДЛЯ ИНИЦИАЛИЗАЦИИ КОНСТАНТ И КАКИХ ЛИБО ПОСТОЯННЫХ ЗНАЧЕНИЙ
"""

import vk_api
import vk_api.keyboard
from vk_api.longpoll import VkLongPoll
from vk_api import VkUpload  # для загрузки картинок на сервер вк
import pyGitConnect
import json
from botlib import dotenv

_env = dotenv.DotEnv()

REGEXP = {
    "url": r"\w{1,}:\/\/.+"
}

GITHUB = pyGitConnect.User(
    token=_env.GITHUB_TOKEN,
    username=_env.GITHUB_NICKNAME,
    email=_env.GITHUB_EMAIL
)
REPOSITORY_NAME = "public-vk-ranepa-mobot"

CONST_FILE = pyGitConnect.File(GITHUB, REPOSITORY_NAME + "/content/const.json")
CONST = json.loads(CONST_FILE.get().decode("utf-8"),
                   parse_int=True, parse_constant=True, parse_float=True)

USERS_CHOICE_FILE = pyGitConnect.File(
    GITHUB,
    REPOSITORY_NAME + "/content/userChoice.json"
)
USERS_CHOICE = json.loads(USERS_CHOICE_FILE.get().decode("utf-8"))

VK = vk_api.VkApi(token=_env.VK_TOKEN)
LONGPOLL = VkLongPoll(VK)
UPLOAD = VkUpload(VK)


class BotKeyboards(object):

    def backToMainMenu():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()

    def main():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Узнать расписание", "positive")
        kb.add_line()
        kb.add_button("Создать список литературы", "positive")
        kb.add_line()
        kb.add_button("Расширение для СДО", "secondary")
        return kb.get_keyboard()

    def choiceDirection():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Экономика", "secondary")
        kb.add_button("Менеджмент", "secondary")
        kb.add_line()
        kb.add_button("ГМУ", "secondary")
        kb.add_button("Юриспруденция", "secondary")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()

    def choiceKurs():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("1", "secondary")
        kb.add_button("2", "secondary")
        kb.add_button("3", "secondary")
        kb.add_button("4", "secondary")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()

    def choiceDirection():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Экономика", "secondary")
        kb.add_button("Менеджмент", "secondary")
        kb.add_line()
        kb.add_button("ГМУ", "secondary")
        kb.add_button("Юриспруденция", "secondary")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()

    def choiceOz():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Очная", "secondary")
        kb.add_button("Очно-заочная", "secondary")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()
        
    def choiceMag():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Бакалавриат", "secondary")
        kb.add_button("Магистратура", "secondary")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()

    def sendReport(user_choice):
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Сообщить об ошибке", "negative")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()

    def choiceSave():
        kb = vk_api.keyboard.VkKeyboard(False, False)
        kb.add_button("Сохранить расписание", "secondary")
        kb.add_line()
        kb.add_button("В главное меню", "positive")
        return kb.get_keyboard()
