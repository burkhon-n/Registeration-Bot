# Registration Bot - Webhook Version

Telegram bot for "O'zbekiston — bag'rikeng diyor!" competition registration using FastAPI webhooks.

## Features

- ✅ Webhook-based bot (production-ready)
- ✅ User registration with step-by-step flow
- ✅ Region and district selection
- ✅ PostgreSQL database integration
- ✅ FastAPI backend server
- ✅ State management for conversation flow
- ✅ **Admin panel with Excel export** (NEW!)
- ✅ Edit personal information
- ✅ Multiple project submissions
- ✅ Project forwarding to channel

## Project Structure

```
.
├── main.py              # FastAPI webhook server
├── bot.py               # Telegram bot handlers
├── config.py            # Configuration settings
├── database.py          # Database connection and setup
├── regions.json         # Regions and districts data
├── models/
│   ├── User.py         # User model
│   └── Address.py      # Address model
└── .env                # Environment variables (create this)
```

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn[standard] pyTelegramBotAPI sqlalchemy psycopg[binary] python-dotenv
```

**Note:** We use `psycopg3` (psycopg[binary]) instead of psycopg2-binary for Python 3.13+ compatibility.

### 2. Setup Database

Create a PostgreSQL database:

```sql
CREATE DATABASE registration_bot;
```

### 3. Configure Environment

Create a `.env` file:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
WEBHOOK_URL=https://yourdomain.com
CHANNEL_ID=@your_channel

# Admin Configuration (comma-separated Telegram user IDs)
ADMIN_IDS=123456789,987654321

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/registration_bot
```

**Admin Setup:**
- Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot)
- Add your ID to ADMIN_IDS (comma-separated for multiple admins)
- See [ADMIN_QUICK_START.md](ADMIN_QUICK_START.md) for details

### 4. Setup Webhook URL

For development, you can use [ngrok](https://ngrok.com/):

```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and set it in your `.env` file as `WEBHOOK_URL`.

## Running the Application

### Development

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000` and automatically set up the webhook.

### Production

Use a process manager like systemd, supervisor, or PM2:

```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000

# Or with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

- `GET /` - Server status
- `POST /webhook/{TOKEN}` - Telegram webhook endpoint
- `GET /health` - Health check
- `GET /webhook-info` - Current webhook information

## Bot Commands

- `/start` - Start the bot and show welcome message
- `👤 Ro'yxatdan o'tish` - Begin registration process
- `🏠 Bosh sahifa` - Return to home page

## Registration Flow

1. **Full Name** - User enters their full name
2. **Region** - User selects their region from 14 regions
3. **District** - User selects their district
4. **Mahalla** - User enters their neighborhood/mahalla name
5. **Workplace** - User enters their workplace
6. **Birth Date** - User enters birth date (DD.MM.YYYY format)
7. **Passport** - User enters passport (AA1234567 format, case-insensitive)
8. **Phone Number** - User shares contact or enters manually
9. **Confirmation** - Review all data with option to edit specific fields
10. **Project Type** - User selects project category:
    - ✍️ Maqola yoki esse (Article/Essay)
    - 🎤 She'r yoki monolog (Poem/Monologue)
    - 🎶 Qo'shiq yoki musiqiy chiqish (Song/Music)
    - 🎨 Rassomchilik ishi (Art)
    - 🧵 Hunarmandchilik namunasi (Crafts)
    - 🎥 Video-rolik yoki kontent (Video)
11. **Project File** - User uploads project file
12. **Auto-forward** - Bot forwards file + user data to designated channel
13. **Completion** - User can submit another project or return home

## Database Models

### User
- `telegram_id` - Unique Telegram user ID
- `full_name` - User's full name
- `address_id` - Foreign key to Address
- `workplace` - User's workplace
- `birth_date` - User's birth date
- `passport_series` - Passport information
- `phone_number` - Contact number
- `project_url` - Project link

### Address
- `region_id` - Region ID from regions.json
- `district_id` - District ID from regions.json
- `neighborhood` - Mahalla/neighborhood name

### Project
- `user_id` - Foreign key to User
- `type` - Project type (essay, poem, song, art, craft, video)
- `project_url` - Telegram channel message URL

## Admin Features

### Export Data to Excel

Admins can export all collected data as a comprehensive Excel file with:

1. **User List** - All registered users with complete information
2. **Project List** - All submitted projects with participant details
3. **Statistics** - Breakdown by regions and project types

**How to use:**
1. Add your Telegram user ID to `ADMIN_IDS` in `.env`
2. Send `/start` to the bot
3. Click "📊 Ma'lumotlarni yuklab olish (Admin)"
4. Download the generated Excel file

**Excel file includes:**
- ✅ Clean, professional formatting
- ✅ Color-coded headers
- ✅ Auto-sized columns
- ✅ Complete statistics
- ✅ Timestamped file names

See [ADMIN_GUIDE.md](ADMIN_GUIDE.md) for detailed documentation.

## Troubleshooting

### Webhook not receiving updates

1. Check if webhook is set correctly:
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getWebhookInfo
```

2. Verify your WEBHOOK_URL is accessible from internet
3. Ensure your SSL certificate is valid (Telegram requires HTTPS)

### Database connection error

1. Verify PostgreSQL is running
2. Check DATABASE_URL format
3. Ensure database exists and user has permissions

### Import errors

Install missing packages:
```bash
pip install -r requirements.txt
```

## Development Tips

- Use ngrok for local webhook testing
- Check logs for errors: `tail -f /var/log/bot.log`
- Monitor database with: `psql -d registration_bot`
- Test webhook manually: Use `/webhook-info` endpoint

## License

MIT License

## Support

For issues and questions, please contact the development team.
