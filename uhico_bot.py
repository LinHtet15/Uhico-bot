import logging
import re
import os
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = "8641878091:AAETYx4TnbbsUOe-rZf4U8fXuvHuiEFLT7s"
ADMIN_ID = 8545074928

# Order storage
orders = []
order_counter = 0

# Dummy web server for Render health check
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Uhico Bot is running!")
    def log_message(self, format, *args):
        pass

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

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

ဥပမာ:
💎 86 diamonds
🔣 ID: 123456789
🔣 Server: 2697

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
    "နံပါတ်",
    "နံပါတ်ပေးပါ",
    "ငွေလွှဲရမဲ့",
    "ဘယ်ကိုပို့ရမလဲ",
    "ဘယ်နံပါတ်",
    "account",
    "acc",
    "ဖုန်းနံပါတ်",
    "လွှဲရမယ့်",
    "လွဲရမယ့်",
]

ORDER_KEYWORDS = [
    "မှာမယ်",
    "order",
    "မှာချင်",
    "ယူမယ်",
    "လိုချင်",
]

GREETING_KEYWORDS = [
    "hi",
    "hello",
    "hey",
    "hihi",
    "ဟိုင်း",
    "ဟယ်လို",
]

GREETING_REPLY = """Hi! Welcome to Uhico Reseller gp 🔥

💎 Diamond ဈေးနှုန်း ကြည့်ရန် - /price
📝 Order တင်နည်း - /order
💸 Payment info - /payment

😺👀🔣@Uhico15🔣✅"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! Welcome to Uhico Reseller gp 🔥\n\n"
        f"💎 Diamond ဈေးနှုန်း ကြည့်ရန် - /price\n"
        f"📝 Order တင်နည်း - /order\n"
        f"💸 Payment info - /payment\n\n"
        f"👑 Admin Commands:\n"
        f"/orders - Pending order list ကြည့်ရန်\n"
        f"/done [order number] - Order ပြီးကြောင်း mark လုပ်ရန်\n\n"
        f"😺👀🔣@Uhico15🔣✅",
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(PRICE_LIST)

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ORDER_INSTRUCTIONS)

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(PAYMENT_INFO)

async def view_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⚠️ Admin only command ဖြစ်ပါတယ်။")
        return
    
    pending = [o for o in orders if o["status"] == "pending"]
    if not pending:
        await update.message.reply_text("✅ Pending order မရှိပါ။")
        return
    
    msg = "📋 Pending Orders:\n\n"
    for o in pending:
        msg += f"🔢 Order #{o['id']}\n"
        msg += f"👤 {o['customer_name']}\n"
        msg += f"💬 {o['details']}\n"
        msg += f"⏰ {o['time']}\n"
        msg += "─────────────\n"
    
    msg += f"\n📊 Total pending: {len(pending)}\n"
    msg += "✅ Order ပြီးရင် /done [number] ရိုက်ပါ"
    await update.message.reply_text(msg)

async def done_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⚠️ Admin only command ဖြစ်ပါတယ်။")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /done [order number]\nExample: /done 1")
        return
    
    try:
        order_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("⚠️ Order number ရိုက်ပါ။ Example: /done 1")
        return
    
    for o in orders:
        if o["id"] == order_id:
            o["status"] = "done"
            await update.message.reply_text(f"✅ Order #{order_id} ပြီးပါပြီ!")
            return
    
    await update.message.reply_text(f"⚠️ Order #{order_id} မတွေ့ပါ။")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global order_counter
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower().strip()
    
    # Check for greeting keywords
    for keyword in GREETING_KEYWORDS:
        if keyword.lower() == text or keyword.lower() in text.split():
            await update.message.reply_text(GREETING_REPLY)
            return

    # Check for price keywords
    for keyword in PRICE_KEYWORDS:
        if keyword.lower() in text:
            await update.message.reply_text(PRICE_LIST)
            return
    
    # Check for payment keywords
    for keyword in PAYMENT_KEYWORDS:
        if keyword.lower() in text:
            await update.message.reply_text(PAYMENT_INFO)
            return
    
    # Check for order keywords
    for keyword in ORDER_KEYWORDS:
        if keyword.lower() in text:
            order_counter += 1
            from datetime import datetime
            order_data = {
                "id": order_counter,
                "customer_name": update.effective_user.full_name,
                "customer_id": update.effective_user.id,
                "details": update.message.text,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "pending"
            }
            orders.append(order_data)
            
            # Reply to customer
            await update.message.reply_text(
                f"✅ Order #{order_counter} received!\n\n"
                f"ငွေလွဲစလစ်၊ ယူမဲ့ dia အမောက်၊ ID နဲ့ Server ID တွဲပို့ပေးပါ။\n"
                f"Admin က စစ်ဆေးပြီး diamond ထည့်ပေးပါမယ်။\n\n"
                f"😺👀🔣@Uhico15🔣✅"
            )
            
            # Notify admin
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"🔔 Order အသစ်!\n\n"
                         f"🔢 Order #{order_counter}\n"
                         f"👤 {update.effective_user.full_name}\n"
                         f"💬 {update.message.text}\n\n"
                         f"✅ ပြီးရင် /done {order_counter} ရိုက်ပါ"
                )
            except Exception as e:
                logger.error(f"Failed to notify admin: {e}")
            return

async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"Welcome {member.full_name} to Uhico Reseller gp 🔥!\n\n"
            f"💎 Diamond ဈေးနှုန်း ကြည့်ရန် - /price\n"
            f"📝 Order တင်နည်း - /order\n"
            f"💸 Payment info - /payment\n\n"
            f"😺👀🔣@Uhico15🔣✅"
        )

def main() -> None:
    # Start health check server in background
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
    logger.info("Health check server started")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("order", order))
    application.add_handler(CommandHandler("payment", payment))
    application.add_handler(CommandHandler("orders", view_orders))
    application.add_handler(CommandHandler("done", done_order))
    application.add_handler(MessageHandler(filters.Regex(r"^/ဈေးနှုန်း"), price))
    application.add_handler(MessageHandler(filters.Regex(r"^/မှာမယ်"), order))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
