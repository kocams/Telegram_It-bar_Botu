import json
import glob
from os import path
from pyrogram import Client, filters
from config import bot_token, owner_id

app = Client(
    "karma",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|teşekkürler|eline sağlık|harika|beğendim|teşekkür ederim|pro|cool|good|👍)$"
regex_downvote = r"^(\-|\-\-|\-1|beğenmedim|kötü|berbat|👎)$"


@app.on_message(filters.command(["start"]))
async def start(_, message):
    await message.reply_text(
        "Bot sorunsuz başlatıldı, hemen grubuna ekle ve o özlenen forum günlerinde olduğu gibi mesajları puanla! \n⚠️: Botun çalışması için yönetici olması şart. \n👨🏻‍🔧: @Mskoca"
    )


@app.on_message(filters.command(["help"]))
async def help(_, message):
    await message.reply_text(
        """Grup içerisindeki herhangi bir mesajı "+" koyarak yanıtlarsanız mesaj sahibinin teşkkür puanını arttırırsınız, "-" koyarak yanıtlarsanız da tam tersi şekilde mesaj sahibinin teşekkür puanını düşürürsünüz. \n/itibar komutunu kullanarak grubun en çok teşekkür alan üyelerini görebilirsiniz."""
    )


@app.on_message(filters.text
                & filters.group
                & filters.incoming
                & filters.reply
                & filters.regex(regex_upvote)
                & ~filters.via_bot
                & ~filters.bot
                & ~filters.edited)
async def upvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not path.exists(filename):
        sample_bot = {"1527962675": 1}
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] += 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(
        f'{user_mention} isimli kullanıcının itibar puanı 1 arttı 👍! \nToplam Puanı: {members[f"{user_id}"]}'
    )


@app.on_message(filters.text
                & filters.group
                & filters.incoming
                & filters.reply
                & filters.regex(regex_downvote)
                & ~filters.via_bot
                & ~filters.bot
                & ~filters.edited)
async def downvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not path.exists(filename):
        sample_bot = {"1527962675": 1}
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] -= 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(
        f'{user_mention} isimli kullanıcının itibar puanı 1 azaltıldı 👎! \nToplam Puanı: {members[f"{user_id}"]}'
    )

import operator
@app.on_message(filters.command(["itibar"]) & filters.group)
async def karma(_, message):
    chat_id = message.chat.id
    filename = f"{chat_id}.json"
    with open(filename) as f2:
        members = json.load(f2)
    fmembers = dict(sorted(members.items(), key=operator.itemgetter(1),reverse=True))
    if not message.reply_to_message:
        output = ""
        m = 0
        for i in fmembers.keys():
            try:
                output += f"`{(await app.get_chat(i)).username}: {list(fmembers.values())[m]}`\n"
            except:
                pass
            if m == 10:
                break
            m += 1
        await message.reply_text(output)

    else:
        user_id = message.reply_to_message.from_user.id
        await message.reply_text(f'Total Points: {members[f"{user_id}"]}')


@app.on_message(filters.command(["yedek"]) & filters.user(owner_id))
async def backup(_, message):
    m = await message.reply_text("Çıktı alınıyor...")
    files = glob.glob("*n")
    for i in files:
        await app.send_document(owner_id, i)
    await m.edit("Yedek alındı ve özelden gönderildi.")


app.run()
