# Debugging Guide

If the bot is not responding after you send your name, follow these steps:

## Step 1: Stop any running instances
```bash
# Press Ctrl+C in the terminal where the bot is running
# Or find and kill the process:
ps aux | grep python | grep main.py
kill <process_id>
```

## Step 2: Check your configuration
```bash
.venv/bin/python check_config.py
```

Make sure:
- Bot token starts with a number (e.g., 8324199808:...)
- Webhook URL is your ngrok URL (https://xxxx.ngrok-free.app)
- No trailing slashes in WEBHOOK_URL

## Step 3: Test bot connectivity
```bash
.venv/bin/python test_bot.py
```

This will show:
- If bot token is valid
- Current webhook status
- Any pending updates

## Step 4: Start the bot with logging
```bash
.venv/bin/python run.py
```

Watch the logs for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Database initialized successfully
INFO:     Webhook set to: https://your-ngrok-url.app/webhook/...
```

## Step 5: Test in Telegram
1. Send `/start` to your bot
2. Click "👤 Ro'yxatdan o'tish"
3. Send your full name
4. Watch the terminal logs - you should see:
   ```
   INFO:     Received update: {...}
   INFO:     Processing full name: Your Name from user 123456
   ```

## Common Issues:

### Issue: Bot doesn't respond at all
**Solution**: Check if ngrok is running and webhook URL is correct
```bash
# In another terminal:
ngrok http 8000

# Copy the https URL and update .env file
# Restart the bot
```

### Issue: Bot responds to /start but not to name input
**Cause**: State storage not working
**Solution**: Already fixed in latest bot.py - make sure you're running the updated version

### Issue: "Webhook delivery failed"
**Solution**: Make sure:
1. Server is running (`python run.py`)
2. ngrok is running (`ngrok http 8000`)
3. Webhook URL in .env matches ngrok URL exactly
4. No firewall blocking port 8000

## Manual Test:
You can manually test the webhook endpoint:
```bash
# Check if server is running:
curl http://localhost:8000/

# Check webhook info:
curl http://localhost:8000/webhook-info
```

## Enable Debug Mode:
Edit `main.py` and change logging level:
```python
logging.basicConfig(level=logging.DEBUG)  # Change INFO to DEBUG
```

## Still not working?
1. Check ngrok dashboard: http://127.0.0.1:4040
   - See if requests are coming in
   - Check for any errors

2. Check database connection:
   ```bash
   psql -U burkhonnurmurodov -d registration_bot -c "SELECT * FROM users;"
   ```

3. Share the error logs from terminal for further help

