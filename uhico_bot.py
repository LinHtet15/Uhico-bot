import logging
import re
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = "8641878091:AAETYx4TnbbsUOe-rZf4U8fXuvHuiEFLT7s"

PRICE_LIST = """📌pin‼️သတိ⚠️ငွေလွဲပြီး -ငွေလွဲစလစ် ၊ ယူမဲ့diaအမောက် ၊ id 🔣sever id🔣 အတူတူတွဲပို့ပေးပါ✅
သတိထားပေးပါနော်✅👀

💯MLBB Diamond price📥 

⭐️💎Weekly Pass ➡️6450Ks 🇲🇲

💎Elite W package➡️3500ks🇲🇲
💎Epic M package➡️17000ks🇲🇲

⭐Twilight Pass 💠34500ks 🇲🇲
💎11 ⏩  900 ks🇲🇲
💎22 ⏩ 1800ks🇲🇲
💎55 ⏩ 4500Ks🇲🇲 
💎86 ⏩ 5400Ks 🇲🇲
💎172 ⏩ 10600Ks🇲🇲
💎257 ⏩ 15500Ks 🇲🇲
💎343 ⏩ 20850Ks 🇲🇲
💎429 ⏩ 26100Ks🇲🇲
💎514 ⏩ 31000Ks 🇲🇲
💎600 ⏩ 35700Ks 🇲🇲
💎706 ⏩ 41800Ks 🇲🇲
💎878 ⏩ 52400Ks 🇲🇲
💎963 ⏩ 57300Ks 🇲🇲
💎1049 ⏩ 62650Ks 🇲🇲
💎2195 ⏩ 126400Ks🇲🇲 
💎3688 ⏩ 210900Ks 🇲🇲
💎5532 ⏩ 318500Ks 🇲🇲
💎9288 ⏩ 528900Ks🇲🇲  

💎Diamond 2ဆ💗
အကောင့်တစ်ကောင့်မှာ တစ်ခါပဲနှစ်ဆရပါမယ်💎😊

💎50+50 ➡️ 3500Ks 🇲🇲
💎150+150 ➡️ 10200Ks🇲🇲 
💎250+ 250 ➡️ 16400Ks🇲🇲 
💎500+ 500 ➡️ 33500Ks 🇲🇲

👀ပြေစာတွင် shop လို့ရေးပေးပါ✅"""

ORDER_INSTRUCTIONS = """📌 Order တင်နည်း:

ငွေလွဲပြီး -ငွေလွဲစလစ် ၊ ယူမဲ့diaအမောက် ၊ id 🔣sever id🔣 အတူတူတွဲပို့ပေးပါ✅

😺👀🔣@Uhico15🔣✅"""

PAYMENT_INFO = """💸PAYMENT- Kpay 🇲🇲
                  09442071612 
               Daw Lwin Lwin Oo😻

💸PAYMENT-Wpay⭐
              09789461824
             A Me Me Soe👀

😺👀🔣@Uhico15🔣✅"""

# Keywords for auto-reply
PRICE_KEYWORDS = [
    "ဈေးဘယ်လောက်လဲ",
    "ဈေးဘယ်လောက်",
    "ဘယ်လောက်လဲ",
    "ဈေးနှုန်း",
    "ဈေး",
    "price",
    "how much",
    "ဘယ်လောက်ကျ",
    "ဈေးပြ",
    "ဈေးလား",
    "dia ဈေး",
    "diamond ဈေး",
    "ဈေးရှင်း",
]

PAYMENT_KEYWORDS = [
    "kpay",
    "wpay",
    "k pay",
    "w pay",
    "ငွေလွှဲ",
    "ငွေလွဲ",
    "ဘယ်ကိုလွှဲ",
    "ဘယ်ကိုလွဲ",
    "payment",
    "ငွေပို့",
    "ဘယ်လိုပေးရမလဲ",
    "ဘယ်လိုလွှဲရမလဲ",
    "ဘယ်လိုလွဲရမလဲ",
]


async def start(update: Update, context) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! Welcome to Uhico Reseller gp 🔥\n\n"
        f"💎 Diamond ဈေးနှုန်း ကြည့်ရန် - /price\n"
        f"📝 Order တင်နည်း - /order\n"
        f"💸 Payment info - /payment\n\n"
        f"😺👀🔣@Uhico15🔣✅",
    )


async def price(update: Update, context) -> None:
    await update.message.reply_text(PRICE_LIST)


async def order(update: Update, context) -> None:
    await update.message.reply_text(ORDER_INSTRUCTIONS)


async def payment(update: Update, context) -> None:
    await update.message.reply_text(PAYMENT_INFO)


async def auto_reply(update: Update, context) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    for keyword in PRICE_KEYWORDS:
        if keyword.lower() in text:
            await update.message.reply_text(PRICE_LIST)
            return

    for keyword in PAYMENT_KEYWORDS:
        if keyword.lower() in text:
            await update.message.reply_text(PAYMENT_INFO)
            return


async def welcome_new_members(update: Update, context) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"Welcome {member.full_name} to Uhico Reseller gp 🔥!\n\n"
            f"💎 Diamond ဈေးနှုန်း ကြည့်ရန် - /price\n"
            f"📝 Order တင်နည်း - /order\n"
            f"💸 Payment info - /payment\n\n"
            f"😺👀🔣@Uhico15🔣✅"
        )


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("order", order))
    application.add_handler(CommandHandler("payment", payment))

    application.add_handler(MessageHandler(filters.Regex(r"^/ဈေးနှုန်း"), price))
    application.add_handler(MessageHandler(filters.Regex(r"^/မှာမယ်"), order))

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
