from pyrogram import *
from pyrogram.types import *
from pyrogram.errors.exceptions import *
from io import *
import requests , json , time , uuid , qrcode , html , re
#---------------------------------input data---------------------------------
with open('config.json', 'r') as file:
    config = json.load(file)
admin_telegram_bot = config['admin_telegram_bot']
telegram_bot_token = config['telegram_bot_token']
marzban_panel_username = config['marzban_panel_username']
marzban_panel_password = config['marzban_panel_password']
marzban_panel_domain  = config['marzban_panel_domain']
#---------------------------------create acces token---------------------------------
try:
    token_header = {  "accept" : "application/json" , "Content-Type" : "application/x-www-form-urlencoded" }
    panel_token_data = {"username" : marzban_panel_username , "password" : marzban_panel_password}
    panel_token = requests.post(url=f"https://{marzban_panel_domain}/api/admin/token" , data=panel_token_data)
    if panel_token.status_code == 200 :
        panel_token_back = json.loads(panel_token.text)
        access_token = panel_token_back.get("access_token")
        panel_headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token}"}
        print("\n\n\n\n\n\n\n\n\n\nBOT IS STARTED...\n\n\n\n\n")
    else :
        print(panel_token.text)
        print("\n\n\n\n\n\n\n\n\n\nError...\n\n\n\n\n")
        print("i can't create acces token , please try again and enter true info or contact with spport @erfjab")
        time.sleep(1)
        print("\n\n\n\n\n\n\n\n\n\nPress Ctrl + C and go to github\n\n\n\n\n")
        time.sleep(10)
except Exception as e:
    print(f"i have a error : {str(e)}")
    time.sleep(10)
#---------------------------------connect telgram bot---------------------------------
app = Client(   
    "holderbot",      
    api_id=26410400,
    api_hash="408bf51732560cb81a0e32533b858cbf",
    bot_token=telegram_bot_token,
)
#---------------------------------github star---------------------------------
global sendgithub
sendgithub = 0
#---------------------------------username checker---------------------------------
def is_valid_username(username):
    pattern = re.compile("^[A-Za-z0-9]{3,32}$")
    return bool(re.match(pattern, username))
#---------------------------------telegram start command---------------------------------
@app.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message) :
    chatid = message.chat.id
    firstname = message.from_user.first_name
    if chatid != admin_telegram_bot :
        await client.send_message(chat_id=chatid , text=f"<b>this bot is private...</b>" , parse_mode=enums.ParseMode.HTML)
    if chatid == admin_telegram_bot :
        text = f"<b>hello Dear {firstname}\nTo create a user, please use this template 👇🏻 :</b>\n\n<b>Username, data(GB), date(days)</b>\n\n<code>example: alex 20 30\nexample: maria unlimited 120\nexample: kevin unlimited 80</code> \n\n<b>💬 if you need help : @erfjab\n⭐ What is premium holderbot? click /pro</b>"
        await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML)
#---------------------------------telegram pattern command---------------------------------
@app.on_message(filters.private & filters.command("pattern") & filters.user(admin_telegram_bot) )
async def pattern(client: Client, message: Message) :
    text = "<b>USERNAME VOLUME TIME\n\n◽ username : A-Z 0-9 3-32 character\n◽ volume : unlimited or Number(int)\n◽ time : Number(int)</b>\n\n<code>example: anna 50 30 \nexample: jordi unlimited 120\nexample: erfjab unlimited 30</code> \n\n<b>💬 if you need help : @erfjab</b>"
    await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML)
#---------------------------------telegram pro command---------------------------------
@app.on_message(filters.private & filters.command("pro") & filters.user(admin_telegram_bot))
async def pro(client: Client, message: Message) :
    text = "<b>😍 Premium features :\n\n🔹 Get the pro statistics bot with customize\n🔹 Create admin with volume and time limits\n🔹 Upload the link to the channel/group/PV\n🔹 Create a group of users\n🔹 Desired change of inbound configs\n🔹 Restart user usage\n🔹 Change user volume and time\n🔹 Can reconnect nodes\n🔹 And whatever you want... \n\n💬 if you want premium holderbot or need help , contact me : @erfjab</b>"
    await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML)
#---------------------------------telegram create command---------------------------------
@app.on_message(filters.private & filters.user(admin_telegram_bot))
async def create(client: Client, message: Message) :
    try :
        message_id = message.id
        message_lines = message.text.strip().split(' ')
        global user_name , user_data , user_date 
        if len(message_lines) == 3 and (message_lines[1].isnumeric() or message_lines[1].lower() == "unlimited") and message_lines[2].isnumeric() and is_valid_username(message_lines[0]) :
            user_name = message_lines[0]
            user_data = message_lines[1]
            user_date = int(message_lines[2])
            text = f"<b>◽ Username :</b> {user_name}\n<b>◽ Data limit :</b> {user_data} GB\n<b>◽ Date limit :</b> {user_date} days"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes, create", callback_data='yes'),
                InlineKeyboardButton("No", callback_data=f'no {message_id}')]])
            await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML ,reply_markup=keyboard)
        else :
            text = f"<b>❌ The input method is not correct! /pattern</b>"
            await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML)
    except ValueError :
        error_message = f"<b>❌ Error :</b>\n<code>The day variable must be a number</code>"
        await client.send_message(chat_id=admin_telegram_bot, text=error_message, parse_mode=enums.ParseMode.HTML)        
    except Exception as e :
        error_message = f"<b>❌ Error :</b>\n<code>{str(e)}</code>"
        await client.send_message(chat_id=admin_telegram_bot, text=error_message, parse_mode=enums.ParseMode.HTML)
#---------------------------------telegram fallback & create user---------------------------------
@app.on_callback_query()
async def handle_callback_query(client: Client, query: CallbackQuery):
    data = query.data
    if data == "yes":
        await query.edit_message_text(text="<b>OK, please wait...</b>" , parse_mode=enums.ParseMode.HTML)
        global user_name , user_data , user_date 
        if user_data.lower() == "unlimited" :
            bytedata = 0
        else :
            bytedata = int(user_data) * (1024**3)
        daysdata = user_date * (24*60*60)
        url = f"https://{marzban_panel_domain}/api/user"
        newuuid = uuid.uuid4()
        data={
        "username": user_name,
        "proxies": {
            "vless": {}
        },
        "inbounds": {
            "vless": {
                "VLESS + WS + TLS 1",
                "VLESS + WS + TLS 2",
                "VLESS + WS + TLS 3",
                "VLESS + WS + TLS 4",
                "VLESS + WS + TLS 5",
                "VLESS + WS + TLS 6"
            }
        },
        "expire" : 0,
        "data_limit": bytedata,
        "data_limit_reset_strategy": "no_reset",
        "status": "on_hold",
        "note": "",
        "on_hold_timeout": "2024-11-03T20:30:00",
        "on_hold_expire_duration": daysdata
        }
        data = json.dumps(data)
        responce = requests.post(url=url , headers=panel_headers , data=data)
        await query.message.delete()
        if responce.status_code == 200 :
            url = f"https://{marzban_panel_domain}/api/user/{user_name}"
            responce = requests.get(url=url , headers=panel_headers)
            if responce.status_code == 200 :
                datauser = json.loads(responce.text)
                subscription_url = datauser.get('subscription_url')
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(subscription_url)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                img_bytes_io = BytesIO()
                qr_img.save(img_bytes_io, 'PNG')
                img_bytes_io.seek(0)
                await app.send_photo(chat_id=admin_telegram_bot , photo=img_bytes_io,caption=f"<code>{html.escape(subscription_url)}</code>")
                await client.send_message(chat_id=admin_telegram_bot , text=f"<b>✅ {user_name} | {user_data} GB | {user_date} Days</b>" , parse_mode=enums.ParseMode.HTML) 
                global sendgithub
                if sendgithub == 0 :
                    text = '<b>❤️ If you like it, then give us a <a href="https://github.com/erfjab/holderbot">star on GitHub</a></b>\n(You will not see this message again)'
                    await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML) 
                    sendgithub = 1
            else :
                text = f"<b>❌ i cerated user but I can't send it to you!</b>"
                await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML)   
        else :
            text = f"<b>❌ i can't create user !</b>\n<code>{str(responce.text)}</code>"
            await client.send_message(chat_id=admin_telegram_bot , text=text , parse_mode=enums.ParseMode.HTML) 
    else :
        message_id = int(data.split()[1])
        await query.edit_message_text(text="<b>OK, I forgot...</b>" , parse_mode=enums.ParseMode.HTML)
        time.sleep(2)
        await query.message.delete()
        await client.delete_messages(chat_id=admin_telegram_bot, message_ids=message_id)

app.run()
