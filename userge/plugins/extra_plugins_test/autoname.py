""" Auto Update Name """

# By @Krishna_Singhal
# Base Plugin by @Phyco-Ninja

import asyncio
from collections import deque

from pyrogram.errors import FloodWait

from userge import Message, get_collection, userge

UPDATION = False
AUTONAME_TIMEOUT = 60
NAME = None

CHANNEL = userge.getCLogger(__name__)
LOG = userge.getLogger(__name__)

USER_DATA = get_collection("CONFIGS")

FONTS_ = [
    "abcdefghijklmnopqrstuvwxyz",
    "ð¨ð©ðªð«ð¬ð­ð®ð¯ð°ð±ð²ð³ð´ðµð¶ð·ð¸ð¹ðºð»ð¼ð½ð¾ð¿ðð"
    "ð¦âð§âð¨âð©âðªâð«âð¬âð­âð®âð¯âð°âð±âð²âð³âð´âðµâð¶âð·âð¸âð¹âðºâð»âð¼âð½âð¾âð¿â"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "á´Êá´á´á´ÒÉ¢ÊÉªá´á´Êá´É´á´á´Ç«Êsá´á´á´ á´¡xÊá´¢",
    "â³à¸¿âµÄÉâ£â²â±§ÅJâ­â± â¥â¦Ãâ±Qâ±¤â´â®ÉVâ©Ó¾Éâ±«",
    "Î±Ð²Â¢âÑfgÐ½Î¹× ÐºâÐ¼Ð¸ÏÏqÑÑÑÏÎ½ÏÏÑz",
    "â¶â·â¸â¹âºâ»â¼â½â¾â¿ââââââââââââââââ",
    "ððððððððððððððððð ð¡ð¢ð£ð¤ð¥ð¦ð§ð¨ð©",
    "ð°ð±ð²ð³ð´ðµð¶ð·ð¸ð¹ðºð»ð¼ð½ð¾ð¿ðððððððððð",
    "ð°ð±ð²ð³ð´ðµð¶ð·ð¸ð¹ðºð»ð¼ð½ð¾ð¿ðððððððððð",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ï¼¡ï¼¢ï¼£ï¼¤ï¼¥ï¼¦ï¼§ï¼¨ï¼©ï¼ªï¼«ï¼¬ï¼­ï¼®ï¼¯ï¼°ï¼±ï¼²ï¼³ï¼´ï¼µï¼¶ï¼·ï¼¸ï¼¹ï¼º",
    "Î±Ð²câÎµÒgÐ½Î¹× ÐºâÐ¼Î·ÏÏqÑsÑÏvÏxÒ¯z",
    "åä¹åáªä¹åá¶åä¸¨ï¾Òã¥çªå ãå©Éå°ºä¸ãã©á¯å±±ä¹ãä¹",
    "áªbáá á¬fá¶há¥já¦ámáá¾á¢qásáuáá³xá½á",
    "Î±Éà«®âÎµÆÉ É¦à¹ÊÒ¡âÉ±É³ÏÏÏà«¨à¸£Æ­ÂµÑµÏ×á§Æ¶",
    "aÐ²cdeÒgÐ½Î¹jÄ¸lÐ¼nopqrÑÑÏvwÑyz",
    "ÐÐCDÎFGHIJÒLMÐÐ¤PÇªÐ¯SÎÐ¦VÐ©ÐÐ£Z",
    "ê¬ê³êê¯êê°êêêê»êêêµêê²ê£ê°êªêêê¤ê¦êê§ê¦ê´",
    "à¸áªà¥®á«à«¯Ô²à«­ÒºÉ¿ÊÒÕÉ±Õà«¦Æ¿Ò©ÕÏà©®Ïà±®Ïà«ª×¢àª½",
    "á©á·ááªEá´Gá¼IáKáªá°áOá­á«ááTáá¯á¯á­Yá",
    "áá°áá´áá¦á¶áá¥á á¦áá·áá§á®á¤áááá¬áááá©á",
]


async def _init() -> None:
    global UPDATION, AUTONAME_TIMEOUT, NAME  # pylint: disable=global-statement
    data = await USER_DATA.find_one({"_id": "UPDATION"})
    if data:
        UPDATION = data["on"]
    if UPDATION:
        NAME = data["NametoUpdate"]
    a_t = await USER_DATA.find_one({"_id": "AUTONAME_TIMEOUT"})
    if a_t:
        AUTONAME_TIMEOUT = a_t["data"]


@userge.on_cmd(
    "autoname",
    about={
        "header": "Auto Updates your Profile name with Diffrent Fonts",
        "usage": "{tr}autoname\n{tr}autoname [new name]",
    },
    allow_via_bot=False,
)
async def auto_name(msg: Message):
    global UPDATION, NAME  # pylint: disable=global-statement
    if UPDATION:
        if isinstance(UPDATION, asyncio.Task):
            UPDATION.cancel()
        UPDATION = False

        await USER_DATA.update_one(
            {"_id": "UPDATION"}, {"$set": {"on": False}}, upsert=True
        )
        await asyncio.sleep(1)

        # Reverting Old Name
        data = await USER_DATA.find_one({"_id": "UPDATION"})
        fname = data["fname"]
        await msg.edit("`Setting up Original Name...`")
        await userge.update_profile(first_name=fname)
        await USER_DATA.delete_one({"_id": "UPDATION", "fname": fname})
        await msg.edit(
            "Auto Name Updation is **Stopped** Successfully...", log=__name__, del_in=5
        )
        return
    NAME = msg.input_str
    if not NAME:
        NAME = msg.from_user.first_name
    # Store current name to revert
    first_name = (await userge.get_me()).first_name
    await USER_DATA.update_one(
        {"_id": "UPDATION"},
        {"$set": {"on": True, "fname": first_name, "NametoUpdate": NAME}},
        upsert=True,
    )
    await msg.edit(
        "Auto Name Updation is **Started** Successfully...", log=__name__, del_in=3
    )
    loop = asyncio.get_event_loop()
    UPDATION = loop.create_task(_autoname_worker())


@userge.on_cmd(
    "santo",
    about={
        "header": "Set Auto Name timeout",
        "usage": "{tr}santo [timeout in seconds]",
        "examples": "{tr}santo 30",
    },
)
async def set_name_timeout(message: Message):
    """set Auto Name timeout"""
    global AUTONAME_TIMEOUT  # pylint: disable=global-statement
    t_o = int(message.input_str)
    if t_o < 30:
        await message.err("too short! (minimum 30 sec)")
        return
    await message.edit("`Setting Auto Name timeout...`")
    AUTONAME_TIMEOUT = t_o
    await USER_DATA.update_one(
        {"_id": "AUTONAME_TIMEOUT"}, {"$set": {"data": t_o}}, upsert=True
    )
    await message.edit(f"`Set Auto Name timeout as {t_o} seconds!`", del_in=5)


@userge.on_cmd("vanto", about={"header": "View Auto Name timeout"})
async def view_name_timeout(message: Message):
    """view Auto Name timeout"""
    await message.edit(
        f"`Name will be updated after {AUTONAME_TIMEOUT} seconds!`", del_in=5
    )


@userge.add_task
async def _autoname_worker():
    global UPDATION, NAME, FONTS_  # pylint: disable=global-statement
    animation = "|/-\\"
    anicount = 0
    FONTS_ = deque(FONTS_)
    while UPDATION and NAME:
        F = list(FONTS_)
        cur_list = list(F[0])
        to_rep_list = list(F[1])
        for ch in NAME:
            if not UPDATION:
                break
            if ch in cur_list:
                rep_ch = to_rep_list[cur_list.index(ch)]
                NAME = NAME.replace(ch, rep_ch, 1)
                fname = animation[anicount] + " $ " + NAME + " $ " + animation[anicount]
                try:
                    await userge.update_profile(first_name=fname)
                except FloodWait as s_c:
                    await CHANNEL.log(
                        f"Sleeping for {s_c} seconds because of Autoname."
                    )
                    await asyncio.sleep(s_c.x)
                except Exception as e:
                    LOG.error(e)
                    await CHANNEL.log(f"**ERROR:** `{str(e)}")
                await asyncio.sleep(AUTONAME_TIMEOUT)
                anicount = (anicount + 1) % 4
        FONTS_.rotate(-1)
        await CHANNEL.log("`Switched to New font for AutoName`")
