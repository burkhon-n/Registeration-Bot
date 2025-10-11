# Deployment Checklist

## 1. ✅ Fixed Issues

### Database Driver Update
- ✅ Updated `database.py` to use `psycopg` (version 3) instead of `psycopg2`
- ✅ Automatic URL conversion from `postgresql://` to `postgresql+psycopg://`
- ✅ This works with the `psycopg[binary]==3.2.10` in requirements.txt

### Dependency Updates
- ✅ Updated `aiohttp` from `3.9.1` to `>=3.10.0` (fixes Python 3.13 compatibility)
- ✅ Using `psycopg[binary]` instead of `psycopg2` (no compilation needed)

### Configuration Fixes
- ✅ Updated `Passengerfile.json` paths to `/home/bagriken/repositories/Registeration-Bot`

---

## 2. 📝 Pre-Deployment Steps (Local)

Before uploading to server:

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Fix deployment issues for cPanel"
   git push
   ```

2. **Verify files to upload:**
   - ✅ `database.py` (updated)
   - ✅ `requirements.txt` (updated)
   - ✅ `Passengerfile.json` (updated)
   - ✅ `passenger_wsgi.py`
   - ✅ `cpanel_setup.sh` (new)
   - ✅ All other project files

---

## 3. 🚀 Deployment Steps (On Server)

### Step 1: Upload Files
Upload all files to: `/home/bagriken/repositories/Registeration-Bot/`

### Step 2: Create .env file
Create `/home/bagriken/repositories/Registeration-Bot/.env` with:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
WEBHOOK_URL=https://yourdomain.com
CHANNEL_ID=@your_channel
ADMIN_IDS=123456789,987654321
PORT=8000
HOST=0.0.0.0
```

**Important:** Use standard `postgresql://` format in .env - the code will automatically convert it!

### Step 3: Run Setup Script
```bash
cd ~/repositories/Registeration-Bot
chmod +x cpanel_setup.sh
./cpanel_setup.sh
```

Or manually:
```bash
cd ~/repositories/Registeration-Bot

# Activate virtual environment
source ~/virtualenv/repositories/Registeration-Bot/3.13/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Fix permissions
chmod -R 755 .
find . -type f -name "*.py" -exec chmod 644 {} \;
chmod 755 passenger_wsgi.py

# Restart application
mkdir -p tmp
touch tmp/restart.txt
```

### Step 4: Verify Installation
```bash
# Check if psycopg is installed (NOT psycopg2)
pip list | grep psycopg

# Should see:
# psycopg              3.2.10
# psycopg-binary       3.2.10
```

### Step 5: Test Database Connection
```bash
cd ~/repositories/Registeration-Bot
source ~/virtualenv/repositories/Registeration-Bot/3.13/bin/activate
python -c "from database import engine; print('Database connection successful!')"
```

---

## 4. 🔧 cPanel Python App Configuration

1. Go to **cPanel → Setup Python App**
2. **Create Application** or **Edit** existing:
   - **Python Version:** 3.13
   - **Application Root:** `/home/bagriken/repositories/Registeration-Bot`
   - **Application URL:** Your domain/subdomain
   - **Application Startup File:** `passenger_wsgi.py`
   - **Application Entry Point:** `application`

3. **Add Environment Variables** (optional, if not using .env):
   - `TELEGRAM_BOT_TOKEN`
   - `DATABASE_URL`
   - `WEBHOOK_URL`
   - `CHANNEL_ID`
   - `ADMIN_IDS`

4. Click **Restart** button

---

## 5. ✅ Post-Deployment Verification

### Check Application Status
```bash
# View application logs
tail -f ~/repositories/Registeration-Bot/logs/*.log

# Check if app is running
ps aux | grep passenger

# Test the endpoint
curl https://yourdomain.com
```

### Test Database
```bash
cd ~/repositories/Registeration-Bot
source ~/virtualenv/repositories/Registeration-Bot/3.13/bin/activate
python -c "
from database import SessionLocal, init_db
init_db()
db = SessionLocal()
print('Database tables created successfully!')
db.close()
"
```

### Test Bot Webhook
```bash
curl https://yourdomain.com/webhook/status
```

### Test on Telegram
1. Open your bot on Telegram
2. Send `/start`
3. Verify bot responds

---

## 6. 🐛 Troubleshooting

### If you see "ModuleNotFoundError: No module named 'psycopg2'"
- ✅ **Already fixed** - database.py now uses psycopg3
- Make sure you uploaded the updated `database.py`
- Restart the application: `touch ~/repositories/Registeration-Bot/tmp/restart.txt`

### If you see "Permission denied" errors
```bash
cd ~/repositories/Registeration-Bot
chmod -R 755 .
find . -type f -exec chmod 644 {} \;
chmod 755 passenger_wsgi.py
```

### If Python packages aren't found
```bash
# Make sure you're in the correct virtual environment
source ~/virtualenv/repositories/Registeration-Bot/3.13/bin/activate

# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Restart
mkdir -p tmp
touch tmp/restart.txt
```

### If database connection fails
- Check DATABASE_URL in .env file
- Verify PostgreSQL credentials
- Ensure database exists
- Test connection: `python -c "from database import engine; print(engine)"`

### View Error Logs
```bash
# Application logs
tail -50 ~/repositories/Registeration-Bot/logs/*.log

# Passenger logs
tail -50 ~/logs/passenger.log

# Apache error logs (if accessible)
tail -50 ~/logs/error_log
```

---

## 7. 📊 Monitoring

### Check Application Health
Create a health check endpoint (already in your FastAPI app):
```bash
curl https://yourdomain.com/health
```

### Monitor Logs
```bash
# Real-time log monitoring
tail -f ~/repositories/Registeration-Bot/logs/*.log

# Check for errors
grep -i error ~/repositories/Registeration-Bot/logs/*.log
```

### Restart Application
```bash
cd ~/repositories/Registeration-Bot
touch tmp/restart.txt
```

Or from cPanel Python App interface → Click "Restart"

---

## 8. 🎯 Success Indicators

✅ No "ModuleNotFoundError" for psycopg2  
✅ Application starts without errors  
✅ Database connection successful  
✅ Bot responds to Telegram messages  
✅ Admin panel accessible  
✅ Projects can be submitted  
✅ Files upload correctly  

---

## 9. 📞 Getting Help

If issues persist, gather this information:
1. Output of: `pip list | grep psycopg`
2. Output of: `ls -la ~/repositories/Registeration-Bot/`
3. Content of: `tail -50 ~/logs/passenger.log`
4. Error messages from browser/Telegram
5. Python version: `python --version`

---

## Quick Reference

### Restart Application
```bash
cd ~/repositories/Registeration-Bot && touch tmp/restart.txt
```

### View Logs
```bash
tail -f ~/logs/passenger.log
```

### Update Code
```bash
cd ~/repositories/Registeration-Bot
git pull
pip install -r requirements.txt
touch tmp/restart.txt
```

### Check Status
```bash
ps aux | grep -E "passenger|python"
curl https://yourdomain.com
```
