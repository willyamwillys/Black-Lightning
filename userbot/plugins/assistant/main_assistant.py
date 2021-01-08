#    Copyright (C) Midhun KM 2020
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import io
import re

from telethon import Button, custom, events
from telethon.tl.functions.users import GetFullUserRequest
from userbot.utils import assistant_cmd
from userbot import bot
from userbot.plugins.sql_helper.blacklist_assistant import (
    add_nibba_in_db,
    is_he_added,
    removenibba,
)
from userbot.plugins.sql_helper.botusers_sql import add_me_in_db, his_userid
from userbot.plugins.sql_helper.idadder_sql import (
    add_usersid_in_db,
    already_added,
    get_all_users,
)

@assistant_cmd("start", is_args=False)
async def start(event):
    starkbot = await tgbot.get_me()
    bot_id = starkbot.first_name
    bot_username = starkbot.username
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    vent = event.chat_id
    starttext = f"Hello, {firstname} ! Senang Bertemu Anda, Saya {bot_id},  Bot Asisten. \n\nMy [➤ Master](tg://user?id={bot.uid}) \nAnda Dapat Berbicara / Menghubungi Master Saya Menggunakan Bot Ini. \n\nJika Anda Ingin Asisten Anda Sendiri, Anda Dapat Menerapkan Dari Tombol Di Bawah Ini. \n\nPowered By [WillyamWillys](https://t.me/willyamwillys)"
    if event.sender_id == bot.uid:
        await tgbot.send_message(
            vent,
                message=f"Hai Master, Ini Aku {bot_id}, Asisten Anda ! \nApa yang Ingin Anda Lakukan hari ini ?",
            buttons=[
                [custom.Button.inline("Tampilkan Pengguna 🔥", data="users")],
                [custom.Button.inline("Perintah Untuk Asisten", data="gibcmd")],
                [
                    Button.url(
                        "Tambahkan Saya ke Grup 👥", f"t.me/{bot_username}?startgroup=true"
                    )
                ],
            ],
        )
    else:
        if already_added(event.sender_id):
            pass
        elif not already_added(event.sender_id):
            add_usersid_in_db(event.sender_id)
        await tgbot.send_message(
            event.chat_id,
            message=starttext,
            link_preview=False,
            buttons=[
                [custom.Button.inline("Deploy your Bot ", data="deploy")],
                [Button.url("Help Me ❓", "https://t.me/willyamwillys")],
            ],
        )


# Data's


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"deploy")))
async def help(event):
    await event.delete()
    if event.query.user_id is not bot.uid:
        await tgbot.send_message(
            event.chat_id,
                message="Anda Dapat Menerapkan Userbot ini Di Heroku Dengan Mengikuti Langkah-Langkah Di Bawah Ini, Anda Dapat Melihat Beberapa Panduan Cepat Di Saluran Dukungan Atau Di Bot Asisten Anda Sendiri. \nTerima kasih telah menghubungi saya.",
            buttons=[
                [
                    Button.url(
                        "Deploy Tutorial 📺",
                        "https://www.youtube.com/watch?v=GfZMqrCAqxI",
                    )
                ],
                [Button.url("Need Help ❓", "https://t.me/willyamwillys")],
            ],
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"users")))
async def users(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        total_users = get_all_users()
        users_list = "Daftar Total Pengguna Dalam Bot. \n\n"
        for starked in total_users:
            users_list += ("==> {} \n").format(int(starked.chat_id))
        with io.BytesIO(str.encode(users_list)) as tedt_file:
            tedt_file.name = "userlist.txt"
            await tgbot.send_file(
                event.chat_id,
                tedt_file,
                force_document=True,
                    caption="Total Pengguna Di Bot Anda.",
                allow_cache=False,
            )
    else:
        pass


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"gibcmd")))
async def users(event):
    await event.delete()
    grabon = "Halo, Ini Beberapa Perintah \n➤ /start - Periksa apakah saya Hidup \n➤ /ping - Pong! \n➤ /tr <lang-code> \n➤ /broadcast - Mengirim Pesan Ke semua Pengguna Di Bot \n➤ /id - Menunjukkan ID Pengguna Dan Media. \n➤ /addnote - Menambahkan catatan \n➤ /notes - Menunjukkan Catatan \n➤ /rmnote - Hapus Catatan \n➤ /alive - Apakah saya hidup? \n➤ /bun - Bekerja Dalam Grup, Melarang Pengguna. \n➤ /unbun - Membatalkan Larangan Pengguna dalam Grup \n➤ /prumote - Mempromosikan Pengguna \n➤ /demute - Mendemosikan Pengguna \n➤ /pin - Pin Pesan \n➤ /stats - Menampilkan Pengguna Total Di Bot \n➤ /purge - Balas Dari Pesan yang Ingin Anda Hapus (Bot Anda Harus Admin untuk Menjalankannya) \n➤ /del - Balas Pesan Yang Harus Dihapus (Bot Anda Harus Admin untuk Menjalankannya)"
    await tgbot.send_message(event.chat_id, grabon)


# Bot Permit.
@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def all_messages_catcher(event):
    if is_he_added(event.sender_id):
        return
    if event.raw_text.startswith("/"):
        pass
    elif event.sender_id == bot.uid:
        return
    else:
        await event.get_sender()
        event.chat_id
        sed = await event.forward_to(bot.uid)
        # Add User To Database ,Later For Broadcast Purpose
        # (C) @SpecHide
        add_me_in_db(sed.id, event.sender_id, event.id)


@tgbot.on(events.NewMessage(func=lambda e: e.is_private))
async def sed(event):
    msg = await event.get_reply_message()
    msg.id
    msg_s = event.raw_text
    user_id, reply_message_id = his_userid(msg.id)
    if event.sender_id == bot.uid:
        if event.raw_text.startswith("/"):
            pass
        else:
            await tgbot.send_message(user_id, msg_s)


# broadcast
@tgbot.on(
    events.NewMessage(
        pattern="^/broadcast ?(.*)", func=lambda e: e.sender_id == bot.uid
    )
)
async def sedlyfsir(event):
    msgtobroadcast = event.pattern_match.group(1)
    userstobc = get_all_users()
    error_count = 0
    sent_count = 0
    for starkcast in userstobc:
        try:
            sent_count += 1
            await tgbot.send_message(int(starkcast.chat_id), msgtobroadcast)
            await asyncio.sleep(0.2)
        except Exception as e:
            try:
                logger.info(f"Error : {error_count}\nError : {e} \nUsers : {chat_id}")
            except:
                pass
    await tgbot.send_message(
        event.chat_id,
        f"Siaran Selesai {sent_count} Grup / Pengguna dan saya mendapat {error_count} Kesalahan dan Jumlah Total {len(userstobc)}",
    )


@tgbot.on(
    events.NewMessage(pattern="^/stats ?(.*)", func=lambda e: e.sender_id == bot.uid)
)
async def starkisnoob(event):
    starkisnoob = get_all_users()
    await event.reply(
        f"**Statistik Bot Anda** \nTotal Pengguna Dalam Bot => {len(starkisnoob)}"
    )


@tgbot.on(events.NewMessage(pattern="^/help", func=lambda e: e.sender_id == bot.uid))
async def starkislub(event):
    grabonx = "Halo, Ini Beberapa Perintah \n➤ /start - Periksa apakah saya Hidup \n➤ /ping - Pong! \n➤ /tr <lang-code> \n➤ /broadcast - Mengirim Pesan Ke semua Pengguna Di Bot \n➤ /id - Menunjukkan ID Pengguna Dan Media. \n➤ /addnote - Menambahkan catatan \n➤ /notes - Menunjukkan catatan \n➤ /rmnote - Menghapus catatan \n➤ /alive - Apakah saya hidup? \n➤ /bun - Bekerja Dalam Grup, Melarang Pengguna. \n➤ /unbun - Membatalkan Larangan Pengguna dalam Grup \n➤ /prumote - Promotes A User \n➤ /demute - Mendemosikan Pengguna \n➤ /pin - Pin Pesan \n➤ /stats - Menampilkan Pengguna Total Di Bot"
    await event.reply(grabonx)


@tgbot.on(
    events.NewMessage(pattern="^/block ?(.*)", func=lambda e: e.sender_id == bot.uid)
)
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = his_userid(msg.id)
    if is_he_added(user_id):
        user_id, reply_message_id = his_userid(msg.id)
        await event.reply("Sudah Masuk Daftar Hitam")
    elif not is_he_added(user_id):
        add_nibba_in_db(user_id)
        await event.reply("Memasukkan Orang Bodoh Ini ke dalam daftar hitam")
        await tgbot.send_message(
            user_id, "Anda Telah Masuk Daftar Hitam Dan Anda Tidak Dapat Mengirim Pesan kepada Tuan Saya Sekarang."
        )


@tgbot.on(
    events.NewMessage(pattern="^/unblock ?(.*)", func=lambda e: e.sender_id == bot.uid)
)
async def starkisnoob(event):
    if event.sender_id == bot.uid:
        msg = await event.get_reply_message()
        msg.id
        event.raw_text
        user_id, reply_message_id = his_userid(msg.id)
    if not is_he_added(user_id):
        await event.reply("Bahkan tidak. Masuk daftar hitam 🤦🚶")
    elif is_he_added(user_id):
        removenibba(user_id)
        await event.reply("Lepaskan Orang Bodoh Ini dari Daftar Hitam")
        await tgbot.send_message(
            user_id, "Selamat! Anda Telah Dicabut Daftar Hitam Oleh Tuan Saya."
        )
