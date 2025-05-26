import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace these with your real keys
TELEGRAM_BOT_TOKEN = "8020736200:AAFOEJBI4H4hazpI-eIC25garCClgWi8Mio"
OPENWEATHER_API_KEY = "e01dca6d21ad3bcd0c827da22b55b899"

# Weather fetching function
def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["cod"] != 200:
            return f"City '{city}' not found!"

        weather_desc = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        return (f"🌤️ Weather in *{city.title()}*:\n"
                f"• Description: {weather_desc}\n"
                f"• Temperature: {temp}°C\n"
                f"• Feels Like: {feels_like}°C\n"
                f"• Humidity: {humidity}%")
    except Exception as e:
        return f"Error getting weather: {e}"

# Telegram command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me any city name to get the current weather ☁️")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    await update.message.chat.send_action(action="typing")
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info, parse_mode="Markdown")

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Weather bot is running...")
    app.run_polling()
