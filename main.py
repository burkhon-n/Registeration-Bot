from fastapi import FastAPI, Request, HTTPException
from telebot import types
import asyncio
import config
from database import init_db
from bot import bot
import logging
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress aiohttp ResourceWarning for unclosed sessions in WSGI environment
# This is expected behavior when running under Passenger/WSGI
warnings.filterwarnings("ignore", message=".*Unclosed client session.*", category=ResourceWarning)
warnings.filterwarnings("ignore", message=".*Unclosed connector.*", category=ResourceWarning)

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
    
    # Ensure database is initialized
    if not _db_initialized:
        try:
            await ensure_db_initialized()
        except:
            pass  # Don't block if DB init fails
    
    # Setup webhook on first request
    if not _webhook_set:
        await setup_webhook()
        _webhook_set = True
    
    return {
        "status": "running",
        "message": "Registration Bot Webhook Server",
        "webhook_path": config.WEBHOOK_PATH,
        "database_ready": _db_initialized
    }

# Webhook endpoint for Telegram
@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    """Handle incoming Telegram updates"""
    try:
        # Ensure database is ready
        if not _db_initialized:
            await ensure_db_initialized()
        
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