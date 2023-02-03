import os

def parseCookies(filename=os.getcwd() + "/botlib/cookies.txt"):
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()
    result = {}
    for l in lines:
        if l[0] == "#":
            continue
        try:
            key = l.split("\t")[5].strip()
            value = l.split("\t")[6].strip()
            result[key] = value
        except Exception:
            pass
    return result


def parseHeaders(filename=os.getcwd() + "/botlib/headers.txt"):
    with open(filename, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    result = {}

    for l in lines:
        if l[0] == "#":
            continue
        try:
            key = l.split(":")[0].strip()
            value = l.split(":")[1].strip()
            result[key] = value
        except Exception:
            pass
    return result
