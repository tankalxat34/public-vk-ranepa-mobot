# import parser
import requests
import time
import re
from botlib import parser

LINK_TYPES = {
    "url": 1,
}


TEMPLATE = "{title} — Текст: электронный // {domen}: [сайт]. — URL: {url} (дата обращения: {date})."
_date = time.strftime("%d.%m.20%y")


def getLink(url, typeOfLink=LINK_TYPES["url"]):
    try:
        req = requests.get(url, headers=parser.parseHeaders())
        try:
            _title = re.findall('<title>(.+?)</title>', req.content.decode("UTF-8"))[0] +'.'
        except Exception:
            _title='.'
        try:
            _author = re.findall("[аА]втор[:ы].[аА-яЯ]{0,}.[аА-яЯ]{0,}..[аА-яЯ]{0,}.", req.text)[0]
            _author2 = "/ "+re.findall("[аА]втор[:ы].[аА-яЯ]{0,}.[аА-яЯ]{0,}..[аА-яЯ]{0,}.", req.text)[0]+"."
        except Exception:
            _author = ' '
            _author2 = ' '
        _domen = url.split("/")[2].replace("www.", "", 1)
        _url = url



        return (TEMPLATE.format(author=_author,
                                    author2=_author2,
                                title=_title,
                                domen=_domen,
                                url=_url,
                                date=_date)).strip()

    except Exception:
        return f"Ссылка {url} не была сформирована из-за ошибки!"

if __name__ == "__main__":
    url = "https://moodle.kstu.ru/mod/book/view.php?id=48008"
    print(getLink(url))