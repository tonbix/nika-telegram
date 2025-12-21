from pyrogram.types import Message
from pyrogram.enums import ChatType
from random import random
from configparser import  ConfigParser


async def validate_message(message: Message, botUsername: str) -> tuple | None:
    messageContent: str = ""

    # reading configuration
    config = ConfigParser()
    config.read("config.ini")

    dmChance = config.getfloat("Messages", "DMAnswer")
    randomChance = config.getfloat("Messages", "RandomAnswer")
    triggerChance = config.getfloat("Messages", "TriggerAnswer")
    triggerWords = config.get("Messages", "TriggerWords").split(" ")

    # looking if messsage has any text content
    if message.text or message.caption:
        messageDifferentType = message.media

        if message.text:
            messageContent = message.text
        if message.caption:
            messageContent = message.caption
    else:
        return

    # verifying chat type
    if message.chat.type in (ChatType.CHANNEL, ChatType.BOT):
        return

    
    def onSuccess():
        """
        return on success
        """
        return (messageContent, messageDifferentType)


    # some random based actions
    if message.mentioned:
        print("### mentioned")
        return onSuccess()
    if random() < randomChance:
        print("### random")
        return onSuccess()
    elif random() < dmChance and message.chat.type is ChatType.PRIVATE:
        print("### DM")
        return onSuccess()
    elif random() < triggerChance and any(trigger in messageContent.lower() for trigger in triggerWords):
        print("### trigger")
        return onSuccess()

    return

