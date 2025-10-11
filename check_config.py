#!/usr/bin/env python3
"""Quick config check"""
import config

print("🔍 Configuration Check")
print("=" * 50)
print(f"Bot Token: {config.TOKEN[:10]}...")
print(f"Webhook URL: {config.WEBHOOK_URL}")
print(f"Webhook Path: {config.WEBHOOK_PATH}")
print(f"Full Webhook: {config.WEBHOOK_URL}{config.WEBHOOK_PATH}")
print(f"Host: {config.HOST}")
print(f"Port: {config.PORT}")
print(f"Database: {config.DATABASE_URL}")
print("=" * 50)
