#!/usr/bin/env python3
"""
Test script to verify bot functionality
"""
import asyncio
import sys
from bot import bot, load_regions
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bot():
    """Test bot basic functionality"""
    try:
        # Test bot token
        me = await bot.get_me()
        logger.info(f"✅ Bot connected: @{me.username}")
        
        # Test regions loading
        regions = load_regions()
        logger.info(f"✅ Regions loaded: {len(regions)} regions")
        
        # Test webhook info
        webhook_info = await bot.get_webhook_info()
        logger.info(f"✅ Webhook URL: {webhook_info.url}")
        logger.info(f"   Pending updates: {webhook_info.pending_update_count}")
        if webhook_info.last_error_message:
            logger.warning(f"   Last error: {webhook_info.last_error_message}")
        
        print("\n" + "="*50)
        print("✅ Bot is configured correctly!")
        print("="*50)
        print(f"\nBot username: @{me.username}")
        print(f"Webhook: {webhook_info.url}")
        print(f"Regions loaded: {len(regions)}")
        
        if webhook_info.pending_update_count > 0:
            print(f"\n⚠️  Warning: {webhook_info.pending_update_count} pending updates")
            print("   These updates may be processed when the server starts")
        
    except Exception as e:
        logger.error(f"❌ Error testing bot: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_bot())
