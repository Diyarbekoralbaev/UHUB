import aiohttp
import openai
from eskiz.client import SMSClient


openai_api_key = "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"  # Use your OpenAI API key
appid = 'e5910f3cccef5829b2abfd2e60b5afb0'  # Use your OpenWeatherMap API key


def air_quality(aqi):
    if aqi <= 50:
        data = {
            "aqi": aqi,
            "level": "Good",
            "color": "#00e400",
            "implications": "Air quality is considered satisfactory, and air pollution poses little or no risk",
            "cautionary": "None"
        }
        return data
    elif aqi <= 100 and aqi > 50:
        data = {
            "aqi": aqi,
            "level": "Moderate",
            "color": "#ffff00",
            "implications": "	Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.",
            "cautionary": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion"
        }
        return data
    elif aqi <= 150 and aqi > 100:
        data = {
            "aqi": aqi,
            "level": "Unhealthy for Sensitive Groups",
            "color": "#ff7e00",
            "implications": "Members of sensitive groups may experience health effects. The general public is not likely to be affected.",
            "cautionary": "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion."
        }
        return data
    elif aqi <= 200 and aqi > 150:
        data = {
            "aqi": aqi,
            "level": "Unhealthy",
            "color": "#ff0000",
            "implications": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects",
            "cautionary": "Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion"
        }
        return data
    elif aqi <= 300 and aqi > 200:
        data = {
            "aqi": aqi,
            "level": "Very Unhealthy",
            "color": "#8f3f97",
            "implications": "Health warnings of emergency conditions. The entire population is more likely to be affected.",
            "cautionary": "Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion."
        }
        return data
    elif aqi > 300:
        data = {
            "aqi": aqi,
            "level": "Hazardous",
            "color": "#7e0023",
            "implications": "Health alert: everyone may experience more serious health effects",
            "cautionary": "Everyone should avoid all outdoor exertion"
        }
        return data

client = SMSClient(
    api_url="https://notify.eskiz.uz/api/",
    email="diyarbekdev@gmail.com",
    password="EdnkqFQpEvEOxUH5vOKhU8oGwrXGo5Gyz6a01z4a",
)

async def fetch_air_quality(lat, lon):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={appid}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print("Failed to fetch data")
                return None

async def get_aqi_level(latitude, longitude):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token=361cb6093b99301f665c15f9f5640e1a64a05a44"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['data']['aqi']
            else:
                print("Failed to fetch data")
                return None



async def get_aqi_info(latitude, longitude):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token=361cb6093b99301f665c15f9f5640e1a64a05a44"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                aqi = data['data']['aqi']
                return air_quality(aqi)
                


async def get_health_recommendations(lat, lon, max_tokens=None):
    openai.api_key = openai_api_key
    
    data = await fetch_air_quality(lat, lon)
    aqi_level = await get_aqi_level(lat, lon)

    pollutants = data['list'][0]['components']
    prompt = f"The current air quality index (AQI) is {aqi_level}, with pollutant concentrations as follows: " \
             f"CO: {pollutants['co']} μg/m3, NO: {pollutants['no']} μg/m3, NO2: {pollutants['no2']} μg/m3, " \
             f"O3: {pollutants['o3']} μg/m3, SO2: {pollutants['so2']} μg/m3, PM2.5: {pollutants['pm2_5']} μg/m3, " \
             f"PM10: {pollutants['pm10']} μg/m3, NH3: {pollutants['nh3']} μg/m3. Based on these levels, " \
             f"what are the recommended health precautions for the general public and sensitive groups?"

    # Using the chat API for a conversational model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ensure you're using a model suitable for chat
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant providing health recommendations based on air quality levels."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        
    )
    
    return response.choices[0].message['content'].strip()



async def send_sms(number, message):
    resp = client._send_sms(
        phone_number=number,
        message=message,
    )
    return resp

async def send_health_recommendations(lat, lon, number):
    message = get_health_recommendations(lat, lon, max_tokens=100)
    return send_sms(number, message)

