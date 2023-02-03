"""
File Parser `.env`

(c) tankalxat34 - 2022
"""
import pathlib
import re

class DotEnv:
    def __init__(self, path: str = pathlib.Path(pathlib.Path().resolve(), ".env"), parse_int: bool = True, parse_float: bool = True, encoding: str = "UTF-8"):
        """
        Class for work with file `.env`

        :param path - path to file `.env`
        """

        ptrn1 = "(.+)\=(\"[^\"]*[^\"]\")|(.+)\=(\'[^\']*.+[^\']\')" # все кавычки
        ptrn2 = "(.+)\=([^\"|\'].*[\ |\n])" # всё без кавычек, но с комментариями

        string = open(path, "r", encoding=encoding).read()

        result = re.findall(ptrn1, string)
        result.extend(re.findall(ptrn2, string))

        for var_line in result:
            if var_line[0] and var_line[1]:
                k = var_line[0]
                v = var_line[1]
            else:
                k = var_line[2]
                v = var_line[3]

            last_value = v.replace("\'", "").replace('"', "").strip()
            if parse_float and "." in v:
                try:
                    last_value = float(last_value)
                except ValueError:
                    pass
            elif parse_int:
                try:
                    last_value = int(last_value)
                except ValueError:
                    pass
            self.__setattr__(k, last_value)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self) -> str:
        return f"DotEnv({self.__dict__})"

    def get(self, key: str) -> any:
        return self.__dict__[key]


if __name__ == "__main__":
    _env = DotEnv()

    print(_env)
    print(_env.GITHUB_TOKEN)
    # print(_env.PRIVATE_KEY)
    # print(_env.get())