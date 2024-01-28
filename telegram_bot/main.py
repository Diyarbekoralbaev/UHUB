from aiogram import Bot, Dispatcher, executor, types
from function import *
from aiogram.dispatcher import FSMContext   
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import *
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # I

BOT_TOKEN = "6983773366:AAEYIKvl9xcz_m5vJRd8ZQqNJ8NUZPZ9NYg"

class check_air(StatesGroup):
    location = State()
    
class get_recomentation(StatesGroup):
    location = State()

class send_requesttt(StatesGroup):
    title = State()
    description = State()
    file_url = State()
    

class Phone(StatesGroup):
    number = State()
    
    


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

loc = types.ReplyKeyboardMarkup(resize_keyboard=True)
loc1 = types.KeyboardButton('Send location', request_location=True)
loc.add(loc1)

main = types.ReplyKeyboardMarkup(resize_keyboard=True)
main1 = types.KeyboardButton('Air Quality')
main2 = types.KeyboardButton('Health Advice')
main3 = types.KeyboardButton('Send Request')
main4 = types.KeyboardButton('Connect phone number')
main.add(main1, main2, main3, main4)


RM = types.ReplyKeyboardRemove()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hello, I'm a bot that can help you with air quality and health advice", reply_markup=main)
    



@dp.message_handler(lambda message: message.text == "Air Quality")
async def air_quality(message: types.Message):
    await message.reply("Send me your location", reply_markup=loc)
    await check_air.location.set()

@dp.message_handler(state=check_air.location, content_types=['location'])
async def air_quality(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    air_quality_data = await get_aqi_info(lat, lon)
    preprocess_data = f"Air Quality Data:\n\nAQI: {air_quality_data['aqi']}\nLevel: {air_quality_data['level']}\nImplications: {air_quality_data['implications']}\nCautionary: {air_quality_data['cautionary']}"
    await message.reply(preprocess_data, reply_markup=main)
    await state.finish()
    
    


@dp.message_handler(lambda message: message.text == "Health Advice")
async def health_advice(message: types.Message):
    await message.reply("Send me your location", reply_markup=loc)
    await get_recomentation.location.set()

@dp.message_handler(state=get_recomentation.location, content_types=['location'])
async def health_advicee(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    health_advice = await get_health_recommendations(lat, lon)
    await message.reply(f"Health Advice:\n{health_advice}", reply_markup=main)
    await state.finish()



@dp.message_handler(lambda message: message.text == "Send Request")
async def send_request(message: types.Message):
    await message.reply("Send me your request title", reply_markup=RM)
    await send_requesttt.title.set()

@dp.message_handler(state=send_requesttt.title)
async def send_request(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.reply("Send me your request description")
    await send_requesttt.description.set()    
    
@dp.message_handler(state=send_requesttt.description)
async def send_request(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.reply("Send me file for your request")
    await send_requesttt.file_url.set()
    

@dp.message_handler(state=send_requesttt.file_url, content_types=['document', 'photo', 'video'])
async def send_request(message: types.Message, state: FSMContext):
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{message.document.file_id}"
    await state.update_data(file_url=file_url)
    data = await state.get_data()
    title = data.get("title")
    description = data.get("description")
    file_url = data.get("file_url")
    await message.reply(f"Your request:\nTitle: {title}\nDescription: {description}\nFile: {file_url}")
    await message.reply("Your request is sent to the administrator", reply_markup=main)
    await add_request(title, description, file_url)


@dp.message_handler(lambda message: message.text == "Connect phone number")
async def connect_phone_number(message: types.Message):
    await message.reply("Send me your phone number", reply_markup=RM)
    await Phone.number.set()
    
@dp.message_handler(state=Phone.number)
async def connect_phone_numberssss(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    number = data.get("number")
    await message.reply(f"Your phone number: {number}")
    await message.reply("Your phone number is connected", reply_markup=main)
    await send_health_recommendations(41,61, number)
    await state.finish()

    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)