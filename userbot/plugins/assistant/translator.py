# Copyright (C) Midhun KM
#
# Please Don't Kang Without Credits
# A Plugin For Assistant Bot
# x0x

import emoji
from googletrans import Translator
from telethon import events


@tgbot.on(events.NewMessage(pattern="^/tr ?(.*)"))
async def _(event):
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "gu"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await tgbot.send_message(
            event.chat_id, "`.tr LanguageCode` sebagai balasan pesan"
        )
        return
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    translated = translator.translate(text, dest=lan)
    after_tr_text = translated.text
    output_str = (
        f"**Diterjemahkan oleh WillyamWillys Assistant Bot** \n"
        f"Sumber {translated.src} \nTerjemahan {lan} \nYang Dapat Saya Terjemahkan Dari Ini {after_tr_text}"
    )
    try:
        await tgbot.send_message(event.chat_id, output_str)
    except Exception:
        await tgbot.send_message(event.chat_id, "Ada yang salah 🤔")
