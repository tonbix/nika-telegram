from dotenv import load_dotenv
from os import getenv
from configparser import ConfigParser

from time import time

from hydrogram import Client                                     # type:ignore
from hydrogram.types import Message
from hydrogram.enums import ChatAction, ChatType
from hydrogram.filters import incoming, command

from utils import validate_message
from utils import format_message

# reading configs and env
load_dotenv()
API_ID, API_HASH = str(getenv("TG_TOKEN")).split(":")   # split token to id and hash

config = ConfigParser()
config.read("config.ini")

if config:
    includedChats = config.get("Messages", "IncludedChats").split(" ")
    answerDM = config.getboolean("Messages", "AnswerDM")

with open("initPrompt", "r") as initPromptFile:
    initPrompt = initPromptFile.read()

# initializing bot
app = Client("nika", API_ID, API_HASH)


@app.on_message(command("help", prefixes="."))
async def command_help(_ , message: Message) -> None:
   helpText = " 📚 доступные команды\n.geninit : создает образ, основанный на сообщениях пользователя чата. Без аргументов выбирает пользователя случайно"
   
   await message.reply_text(helpText)

@app.on_message(incoming)
async def message_handler(client: Client, message: Message) -> None:
    print(message.chat.id, includedChats)
    print(answerDM, message.chat.type == ChatType.PRIVATE)
    if not ( message.chat.id in includedChats ) or not ( answerDM and message.chat.type == ChatType.PRIVATE ):
        return

    startTime = time()
    botUsername = (await client.get_me()).username
    content = await validate_message(message=message, botUsername=botUsername)

    if content:
        formattedContent = await format_message(message, content[1])
        timeDelta = round((time() - startTime) * 1000, 3)

        print(f" --- handled {message.id} from {message.chat.id}: {content}")
        print(f"prompted ai with: \"\"\"\n | {formattedContent.replace("\n", "\n | ")}\n\"\"\"")
        print(f"time to answer {timeDelta}ms")
        print(f"answered with: {0}\n")
    else:
        return


def main() -> None:
    app.run()


if __name__=="__main__":
    botName = "N.I.K.A (mk2)"
    print(f" {botName} is running\n")
    main()
    print(f"\n {botName} stopped")

