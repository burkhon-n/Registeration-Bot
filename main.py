from fastapi import FastAPI, Request, HTTPException
from telebot import types
import asyncio
import config
from database import init_db
from bot import bot
import logging
import warnings
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

app_file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'app.log'),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
app_file_handler.setLevel(logging.INFO)

error_file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'error.log'),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
error_file_handler.setLevel(logging.ERROR)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
app_file_handler.setFormatter(formatter)
error_file_handler.setFormatter(formatter)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, app_file_handler, error_file_handler]
)

logger = logging.getLogger(__name__)

# Suppress aiohttp ResourceWarning for unclosed sessions in WSGI environment
# This is expected behavior when running under Passenger/WSGI
warnings.filterwarnings("ignore", message=".*Unclosed client session.*", category=ResourceWarning)
warnings.filterwarnings("ignore", message=".*Unclosed connector.*", category=ResourceWarning)

# Log startup
logger.info("=" * 60)
logger.info("Registration Bot Starting")
logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logger.info(f"Log directory: {log_dir}")
logger.info("=" * 60)

# Initialize FastAPI app
app = FastAPI(title="Registration Bot", version="1.0.0")

# Flag to track if initialization has been done
_initialized = False

def initialize_app():
    """Initialize application - called by passenger_wsgi.py"""
    global _initialized
    if not _initialized:
        try:
            # Initialize database (but don't fail if DB is not accessible yet)
            try:
                init_db()
                logger.info("Database initialized successfully")
            except Exception as db_error:
                logger.warning(f"Database initialization deferred: {db_error}")
                logger.info("Database will be initialized on first request")
            _initialized = True
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            # Don't raise - allow app to start even if DB is not ready

async def setup_webhook():
    """Setup Telegram webhook - called lazily on first request"""
    try:
        webhook_url = f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}"
        await bot.remove_webhook()
        await bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to: {webhook_url}")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")

# Track if webhook has been set
_webhook_set = False
_db_initialized = False

async def ensure_db_initialized():
    """Ensure database is initialized (lazy initialization)"""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            logger.info("Database initialized (lazy)")
            _db_initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - simple status check and lazy webhook setup"""
    global _webhook_set
    
    logger.info("Root endpoint accessed")
    
    # Ensure database is initialized
    if not _db_initialized:
        try:
            await ensure_db_initialized()
        except Exception as e:
            logger.warning(f"Database initialization failed on root access: {e}")
            pass  # Don't block if DB init fails
    
    # Setup webhook on first request
    if not _webhook_set:
        logger.info("Setting up webhook on first request")
        await setup_webhook()
        _webhook_set = True
    
    response = {
        "status": "running",
        "message": "Registration Bot Webhook Server",
        "webhook_path": config.WEBHOOK_PATH,
        "database_ready": _db_initialized
    }
    logger.info(f"Root endpoint response: {response}")
    return response

# Webhook endpoint for Telegram
@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    """Handle incoming Telegram updates"""
    try:
        # Ensure database is ready
        if not _db_initialized:
            logger.info("Initializing database on webhook request")
            await ensure_db_initialized()
        
        json_data = await request.json()
        logger.info(f"Received webhook update: update_id={json_data.get('update_id')}")
        
        # Log message details if present
        if 'message' in json_data:
            msg = json_data['message']
            user_id = msg.get('from', {}).get('id', 'unknown')
            chat_id = msg.get('chat', {}).get('id', 'unknown')
            text = msg.get('text', msg.get('caption', '<no text>'))
            logger.info(f"Message from user {user_id} in chat {chat_id}: {text[:50]}")
        
        update = types.Update.de_json(json_data)
        await bot.process_new_updates([update])
        logger.info("Webhook processed successfully")
        return {"ok": True}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "message": "Bot is running"}

# Webhook info endpoint
@app.get("/webhook-info")
async def webhook_info():
    """Get webhook information"""
    try:
        logger.info("Webhook info endpoint accessed")
        info = await bot.get_webhook_info()
        logger.info(f"Webhook status: url={info.url}, pending={info.pending_update_count}")
        return {
            "url": info.url,
            "has_custom_certificate": info.has_custom_certificate,
            "pending_update_count": info.pending_update_count,
            "last_error_date": info.last_error_date,
            "last_error_message": info.last_error_message,
            "max_connections": info.max_connections,
        }
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))