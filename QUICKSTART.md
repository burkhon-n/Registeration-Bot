# Quick Start Guide 🚀

This guide will help you get the Registration Bot up and running in minutes.

## Prerequisites

- Python 3.13+
- PostgreSQL installed and running
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

## Quick Setup (5 minutes)

### 1. Run the setup script
```bash
./setup.sh
```

This will:
- Create `.env` file from template
- Check PostgreSQL installation
- Install Python dependencies
- Optionally create the database

### 2. Get your Bot Token
1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token you receive

### 3. Configure environment
Edit `.env` file:
```bash
nano .env  # or use your favorite editor
```

Fill in:
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
WEBHOOK_URL=https://your-domain.com
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/registration_bot
```

### 4. For Local Development (with ngrok)

If you're testing locally, you need a public URL:

```bash
# Install ngrok if you haven't
brew install ngrok

# Start ngrok
ngrok http 8000
```

Copy the `https://` URL from ngrok (e.g., `https://abc123.ngrok.io`) and paste it in `.env`:
```env
WEBHOOK_URL=https://abc123.ngrok.io
```

### 5. Start the bot
```bash
python3 main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Webhook set successfully
```

### 6. Test your bot
1. Open Telegram
2. Search for your bot by username
3. Send `/start`
4. Click "👤 Ro'yxatdan o'tish" to begin registration

## Troubleshooting

### Database connection failed
```bash
# Check if PostgreSQL is running
brew services list

# Start PostgreSQL if needed
brew services start postgresql@16

# Create database manually
createdb -U postgres registration_bot
```

### Webhook errors
- Make sure ngrok is running (for local dev)
- Check that WEBHOOK_URL in `.env` matches your ngrok URL
- Verify bot token is correct

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Production Deployment

For production, replace ngrok with a real domain:

1. Deploy to a server with a domain (e.g., Heroku, DigitalOcean, AWS)
2. Set up SSL certificate (Let's Encrypt)
3. Update `WEBHOOK_URL` to your domain: `https://yourdomain.com`
4. Run with a process manager:
   ```bash
   # Using systemd or supervisor
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Need Help?

Check `README.md` for detailed documentation or review the code:
- `bot.py` - Bot handlers and logic
- `main.py` - FastAPI server
- `database.py` - Database connection
- `models/` - Data models

## Next Steps

Once the bot is running:
1. Test the complete registration flow
2. Check database records: `psql -U postgres -d registration_bot -c "SELECT * FROM users;"`
3. Customize the bot messages in `bot.py`
4. Add more features as needed

---

**Happy coding! 🎉**
