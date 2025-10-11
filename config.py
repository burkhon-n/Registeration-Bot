import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://yourdomain.com")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel")  # Channel where projects will be forwarded

# Admin Configuration - comma-separated list of telegram user IDs
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/registration_bot"
)

PROJECT_TYPES = {
    'essay': {
        'title': "✍️ Maqola yoki esse",
        'file_types': "doc, docx, pdf"
    },
    'poem': {
        'title': "🎤 She'r yoki monolog",
        'file_types': "doc, docx, pdf"
    },
    'song': {
        'title': "🎶 Qo'shiq yoki musiqiy chiqish",
        'file_types': "mp3, wav"
    },
    'art': {
        'title': "🎨 Rassomchilik ishi",
        'file_types': "jpg, png, gif"
    },
    'craft': {
        'title': "🧵 Hunarmandchilik namunasi",
        'file_types': "jpg, png, pdf"
    },
    'video': {
        'title': "🎥 Video-rolik yoki kontent",
        'file_types': "mp4, avi"
    }
}