import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database import create_db, add_user, get_all_users
from config import BOT_TOKEN, ADMIN_ID


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

create_db()
users ={}
users_step={}

# Keyboards
city_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Samarkand"), KeyboardButton(text="Tashkent")]
    ],
    resize_keyboard=True
)

phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞Send phone number", request_contact=True)]
    ],
    resize_keyboard=True
)
level_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A1-Beginner"), KeyboardButton(text="A2-Elementary")],
        [KeyboardButton(text="B1-Intermediate"), KeyboardButton(text="B2-Pre-Intermediate")],
        [KeyboardButton(text="C1-Upper-Intermediate"), KeyboardButton(text="C2-Advanced")],
    ],
    resize_keyboard=True
)
admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📃Show all users")]
    ],
    resize_keyboard=True
)
@dp.message(Command("start"))
async def start_handler(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Welcome admin! ", reply_markup=admin_kb)
    else:
        await message.answer(
            "Welcome to Ibrat Speech! 🎤\n\nSend /join to register."
        )

@dp.message(Command("join"))
async def join_handler(message: Message):
    user_id = message.from_user.id
    users_step[user_id] = "name"
    await message.answer("Please enter your full name: ")

@dp.message(lambda message: message.text == "📃Show all users")
async def users_lists(message: Message):
    if message.from_user.id == ADMIN_ID:
        all_users = get_all_users()
        text = "Users list: \n\n"
        for user in all_users:
            text += f"Name: {user[0]} \n Phone: {user[1]}\n Level: {user[2]} \n City: {user[3]} \n\n"
        
        await message.answer(text)

@dp.message(lambda message: message.text)
async def registration_handler(message: Message):
    user_id = message.from_user.id
    
    if user_id not in users_step:
        return
    step = users_step[user_id]
    
    if step =="name":
        users[user_id] ={}
        users[user_id]["name"] = message.text
        users_step[user_id] = "phone"
        await message.answer("Please share your phone number: ", reply_markup=phone_kb)
    
    elif step =="language level":
        users[user_id]["language level"] = message.text
        users_step[user_id] = "city"
        await message.answer("Please choose your city: ", reply_markup=city_kb)
    
    elif step == "city":
        users[user_id]["city"] = message.text
        users_step[user_id] = "done"
        
        name = users[user_id]["name"]
        phone = users[user_id]["phone"]
        l_level = users[user_id]["language level"]
        city = users[user_id]["city"]
        
        add_user(user_id, name, phone,l_level, city)
        
        # Send message to admin 
        await bot.send_message(
            ADMIN_ID,
            f"New user registered! \n\n Name: {name}\nPhone: {phone}\nLanguage Level:{l_level}\nCity: {city}"
        )
        await message.answer(
            "✅ Registration successful!\n\n"
            "Welcome to Ibrat Speech!\n"
            "Join our channel: https://t.me/ibratspeech",
            reply_markup=types.ReplyKeyboardRemove()
        )
@dp.message(lambda message: message.contact is not None)
async def contact_handler(message:Message):
    user_id = message.from_user.id
    
    if users_step.get(user_id) == "phone":
        users[user_id]["phone"] = message.contact.phone_number
        users_step[user_id] = "language level"
        await message.answer("Please choose your English level: ", reply_markup=level_kb)
        
async def main():
    print("Bot is running...")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
