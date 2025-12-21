from configparser import ConfigParser

from pyrogram.types import Message
from pyrogram.enums import MessageMediaType


config = ConfigParser()
config.read("config.ini")

async def format_message(message: Message, messageFormat: MessageMediaType):
    # some configurations
    includeName = config.getboolean("Messages", "IncludeName")
    includeReply = config.getboolean("Messages", "includeReply") 


    async def extractTextFromMessage(msg: Message) -> str:
        if msg.text:
            return msg.text
        elif msg.caption:
            return msg.caption
        else:
            return ""

    # update related message
    sender = message.from_user.username
    content = await extractTextFromMessage(message)

    # reply related message
    replyContent, replySender = None, None
    if message.reply_to_message:
        replySender = message.reply_to_message.from_user.username
        replyContent = await extractTextFromMessage(message.reply_to_message)

    if not content:
        return


    senderFormat = "сообщение от \"{}\":\n"
    textFormat = "\"\"\"\n{}{}\n\"\"\""
    replyFormat = "отвечаю на {}\nотвечающее на {}"

    contentPrefixes = {
            "image": "!СОДЕРЖИТИЗОБРАЖЕНИЕ!\n",
            "video": "!СОДЕРЖИТВИДЕО!\n",
            "sticker": "!СОДЕРЖИТСТИКЕР!\n",
            "animation": "!СОДЕРЖИТГИФКУ!\n",
            "text": ""
    }

    contentPrefix = ""

    match messageFormat:
        case MessageMediaType.PHOTO:
            # contains image
            contentPrefix = contentPrefixes["image"]
        case MessageMediaType.VIDEO:
            # contains video
            contentPrefix = contentPrefixes["video"]
        case MessageMediaType.ANIMATION:
            # contains gif animation
            contentPrefix = contentPrefixes["animation"]
        case MessageMediaType.STICKER:
            # sticker message
            contentPrefix = contentPrefixes["sticker"]
        case _:
            # plain message
            contentPrefix = contentPrefixes["text"]

    # building prompt
    formattedMessage = textFormat.format(contentPrefix, content)
    if includeName:
        formattedMessage = senderFormat.format(sender) + formattedMessage
    
    if message.reply_to_message and includeReply:
        formattedReplyMessage = textFormat.format("", replyContent)
        if includeName:
            formattedReplyMessage = senderFormat.format(replySender) + formattedReplyMessage

        formattedMessage = replyFormat.format(formattedMessage, formattedReplyMessage)

    return formattedMessage
