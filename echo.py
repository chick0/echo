from os import getlogin
from time import time
from json import load
from json import dumps
from urllib.request import Request
from urllib.request import urlopen


def get_hook_urls() -> list:
    try:
        with open("targets.txt", mode="r", encoding="utf8") as t_reader:
            return [x.strip() for x in t_reader.read().split("\n")]
    except FileNotFoundError:
        print("* fail to read targets!")
        print("  create 'targets.txt' to send echo with discord webhook")
        return []


def get_payload() -> dict:
    try:
        # custom payload
        payload = load(open("payload.json", mode="r", encoding="utf8"))
    except FileNotFoundError:
        # default payload
        payload = {
            "content": "server started at <t:{now}:T>",
            "embeds": None,
            "username": "echo from {username}".format(
                username=getlogin()
            ),
            "avatar_url": "https://avatars.githubusercontent.com/u/64462443?size=80"
        }

    if type(payload.get("content")) is str:
        payload['content'] = payload['content'].format(
            now=round(time())
        )

    return payload


def send():
    payload = get_payload()
    for url in get_hook_urls():
        if url.startswith("https://discord.com/"):
            request = Request(
                url=url,
                method="POST",
                data=dumps(payload).encode("utf-8")
            )

            request.add_header("User-Agent", "chick0/echo.py")
            request.add_header("Content-Type", "application/json")
            urlopen(request)
        else:
            print("this url is not discord webook url")


if __name__ == "__main__":
    send()
