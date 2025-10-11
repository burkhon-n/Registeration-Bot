from fastapi import FastAPI, Request, HTTPException
from telebot import types
import asyncio
import config
from database import init_db
from bot import bot
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Registration Bot", version="1.0.0")

@app.on_event("startup")
async def on_startup():
    """Initialize database and set webhook"""
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
        
        # Set webhook
        webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
        await bot.remove_webhook()
        await bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

# Root endpoint
@app.get("/")
async def root():
    # Set webhook info in response
    await bot.delete_webhook()
    await bot.set_webhook(url=f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}")
    await bot.get_webhook_info()  # Ensure webhook is set
    return {
        "status": "running",
        "message": "Registration Bot Webhook Server",
        "webhook_path": config.WEBHOOK_PATH
    }

# Webhook endpoint for Telegram
@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    """Handle incoming Telegram updates"""
    try:
        json_data = await request.json()
        update = types.Update.de_json(json_data)
        await bot.process_new_updates([update])
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Webhook info endpoint
@app.get("/webhook-info")
async def webhook_info():
    """Get current webhook information"""
    try:
        info = await bot.get_webhook_info()
        return {
            "url": info.url,
            "has_custom_certificate": info.has_custom_certificate,
            "pending_update_count": info.pending_update_count,
            "last_error_date": info.last_error_date,
            "last_error_message": info.last_error_message,
            "max_connections": info.max_connections,
            "allowed_updates": info.allowed_updates
        }
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    asyncio.run(on_startup())