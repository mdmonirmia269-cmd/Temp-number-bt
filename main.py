import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# বটের টোকেন
API_TOKEN = '9239200994:AAF1CfmE-CA0fHi6rT0CAxam_3vnOo25Yx0'

# NP Network API কনফিগারেশন
API_BASE_URL = 'https://www.npnetworkbd.com/api/user'
API_KEY = 'YOUR_NP_API_KEY'  # এখানে আপনার আসল NP- API Key বসাবেন

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📞 Get Number", callback_data='get_number'),
        InlineKeyboardButton("💰 Balance", callback_data='balance'),
        InlineKeyboardButton("👥 Refer & Earn", callback_data='refer'),
        InlineKeyboardButton("💬 Support", callback_data='support')
    )
    
    welcome_text = (
        "🤖 **Prime Number | Bot**\n"
        "💀 Hello, and I am a Number Auto Bot!\n\n"
        "🛍️ Select a service from the buttons below:"
    )
    await message.reply(welcome_text, parse_mode="Markdown", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'get_number')
async def process_get_number(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📘 Facebook", callback_data='srv_facebook'),
        InlineKeyboardButton("📱 WhatsApp", callback_data='srv_whatsapp'),
        InlineKeyboardButton("📸 Instagram", callback_data='srv_instagram'),
        InlineKeyboardButton("✈️ Telegram", callback_data='srv_telegram'),
        InlineKeyboardButton("❌ Close", callback_data='back_home')
    )
    await bot.message.edit_text("🦉 **Choose a service:**", parse_mode="Markdown", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data.startswith('srv_'))
async def process_service_selection(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    service_name = callback_query.data.split('_')[1].upper()
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🇲🇦 Morocco (0.20tk)", callback_data=f'getnum_{service_name}_Morocco'),
        InlineKeyboardButton("🔄 Refresh", callback_data=callback_query.data),
        InlineKeyboardButton("⬅️ Back", callback_data='get_number')
    )
    text = f"🌐 **{service_name}**\n🛍️ **Live stock list:**\n\nনিচে উপলব্ধ কান্ট্রি ও প্রাইস দেওয়া হলো:"
    await bot.message.edit_text(text, parse_mode="Markdown", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data.startswith('getnum_'))
async def process_get_number_request(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    parts = callback_query.data.split('_')
    service_name = parts[1]
    country = parts[2]
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔄 Change Number", callback_data=f'srv_{service_name.lower()}'),
        InlineKeyboardButton("🌐 Change Country", callback_data='get_number'),
        InlineKeyboardButton("🏠 Home", callback_data='back_home'),
        InlineKeyboardButton("📢 OTP Group", url='https://t.me/YourOTPGroup')
    )
    text = (
        f"🔴 **Country : {country.upper()}-{service_name}-UNKNOWN-NEW-2**\n\n"
        f"🔄 **Waiting for OTP**\n\n"
        f"📱 **Number:** `+212768826110`"
    )
    await bot.message.edit_text(text, parse_mode="Markdown", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'back_home')
async def back_to_home(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📞 Get Number", callback_data='get_number'),
        InlineKeyboardButton("💰 Balance", callback_data='balance'),
        InlineKeyboardButton("👥 Refer & Earn", callback_data='refer'),
        InlineKeyboardButton("💬 Support", callback_data='support')
    )
    welcome_text = (
        "🤖 **Prime Number | Bot**\n"
        "💀 Hello, and I am a Number Auto Bot!\n\n"
        "🛍️ Select a service from the buttons below:"
    )
    await bot.message.edit_text(welcome_text, parse_mode="Markdown", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['balance', 'refer', 'support'])
async def other_sections(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    data = callback_query.data
    if data == 'balance':
        text = "💰 **Account Balance:**\nআপনার বর্তমান ব্যালেন্স: `0.00 TK`"
    elif data == 'refer':
        text = "👥 **Refer & Earn:**\nআপনার রেফারেল লিংক শেয়ার করে আয় করুন!"
    else:
        text = "💬 **Support:**\nযেকোনো সমস্যায় আমাদের সাপোর্টে যোগাযোগ করুন।"
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Back", callback_data='back_home'))
    await bot.message.edit_text(text, parse_mode="Markdown", reply_markup=markup)

if __name__ == '__main__':
    print("Bot is successfully running...")
    executor.start_polling(dp, skip_updates=True)
