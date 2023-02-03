"""
Module for parse webpage with *.pdf schedule file
"""
import urllib.parse
import requests
import re
import time
import vk_api.keyboard
import os

from botlib import parser

LINK = {}
LINK["base"] = "https://mo.ranepa.ru/studentam-i-slushatelyam/"
LINK["eim"] = LINK["base"] + "fakultet-ekonomiki-i-menedzhmenta/raspisanie.php"
LINK["gmu"] = LINK["base"] + \
    "fakultet-gosudarstvennogo-upravleniya-i-prava/raspisanie.php"
LINK["utm"] = "?utm_source=mo.ranepa.ru&utm_medium=referral&utm_campaign=mo.ranepa.ru&utm_referrer=mo.ranepa.ru"

DIRECTIONS_LIST = ["экономика", "менеджмент", "гму", "юриспруденция"]
KURS = ["1", "2", "3", "4"]
OZ = ["очная", "очно-заочная"]
MAG = ["бакалавриат", "магистратура"]

DIRECTION_NAME = {}
DIRECTION_NAME["экономика"] = "E"
DIRECTION_NAME["менеджмент"] = "M"

DIRECTION_NAME["гму"] = "GMY"
DIRECTION_NAME["юриспруденция"] = "YUR"

SCHEDULE_REGEXP = "\(.+\.pdf"

COOKIES = parser.parseCookies()
HEADERS = parser.parseHeaders()


def _createRegExpPattern(direction: str, kurs: int, mag: bool, oz: bool, existingPattern=SCHEDULE_REGEXP):
    """Создает на базе существующего паттерна новый паттерн в зависимости от переданных условий"""
    if mag:
        if direction in [DIRECTION_NAME["экономика"], DIRECTION_NAME["менеджмент"]]:
            local_pattern = "[M-m][A-a][G-g]" + \
                str(kurs) + direction + existingPattern
        else:
            local_pattern = str(kurs) + direction + \
                "\_[M-m][A-a][G-g]\_" + existingPattern
    else:
        if oz:
            if direction in [DIRECTION_NAME["экономика"], DIRECTION_NAME["менеджмент"]]:
                local_pattern = str(kurs) + direction + \
                    "\_[O-o][Z-z]\_" + "\d{1,}\.pdf"
            else:
                local_pattern = str(kurs) + direction + \
                    "\_[O-o][Z-z]\_" + existingPattern
        else:
            local_pattern = str(kurs) + direction + existingPattern

    return local_pattern


def sortForDates(timestamps):
    """Сортирует по датам в Российском формате"""
    timestamps.sort(key=lambda x: time.mktime(
        time.strptime(x[:10], "%d.%m.%Y")))
    return timestamps


class ScheduleChecker:
    def __init__(self, direction: str, kurs: int, mag: bool, oz: bool):
        """Класс для работы с расписанием на сайте"""
        self.direction = direction
        self.kurs = kurs
        self.mag = mag
        self.oz = oz

        if self.direction == DIRECTION_NAME["экономика"] or self.direction == DIRECTION_NAME["менеджмент"]:
            self.LINK_FOR_REQUEST = LINK["eim"]
        elif self.direction == DIRECTION_NAME["гму"] or self.direction == DIRECTION_NAME["юриспруденция"]:
            self.LINK_FOR_REQUEST = LINK["gmu"]
        else:
            return "Invalid link"

        self.REGEXP_PATTERN = _createRegExpPattern(
            self.direction, self.kurs, self.mag, self.oz)

    def getList(self) -> list:
        with requests.Session() as session:
            self.r = session.get(self.LINK_FOR_REQUEST,
                                 headers=HEADERS, cookies=COOKIES)

        schedule_list = list(set(re.findall(self.REGEXP_PATTERN, self.r.text)))
        schedule_list.sort()

        return schedule_list

    def getDates(self) -> list:
        return sortForDates(list(re.findall("\d{2}\.\d{2}\.\d{4}\-\d{2}\.\d{2}\.\d{4}", self.r.text)))

    def getVkKeyboardsList(self) -> list:
        keyboards = []
        for label in self.getList():
            local_kb = vk_api.keyboard.VkKeyboard(one_time=False, inline=True)
            local_kb.add_openlink_button(urllib.parse.unquote(label), self.LINK_FOR_REQUEST[:-4] + "/" + label)
            keyboards.append(local_kb.get_keyboard())
        return keyboards


if __name__ == "__main__":
    schedule = ScheduleChecker(DIRECTION_NAME["экономика"], 1, False, False)
    print(schedule.getList())
    print(schedule.getDates())
    print(schedule.getVkKeyboardsList())

