# ⚡ Quick Fix - Database Connection Error

## The Error
```
[Errno -2] Name or service not known
```

## The Cause
Your DATABASE_URL in `.env` has an **incorrect hostname** or **database doesn't exist**.

---

## 🔧 Quick Fix Steps

### 1. Check your .env file on server:
```bash
cd ~/repositories/Registeration-Bot
cat .env | grep DATABASE_URL
```

### 2. Common DATABASE_URL formats for cPanel:

```env
# Standard format:
DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# Example for cPanel (username: bagriken):
DATABASE_URL=postgresql://bagriken:YOUR_PASSWORD@localhost:5432/bagriken_registration_bot
```

### 3. Verify database exists:
```bash
# Via cPanel: PostgreSQL Databases → Check if database exists
# Or via command line:
psql -U bagriken -h localhost -l
```

### 4. Create database if missing:
```bash
createdb -U bagriken bagriken_registration_bot
# Or use cPanel: PostgreSQL Databases → Create Database
```

### 5. Update .env and restart:
```bash
nano ~/repositories/Registeration-Bot/.env
# Fix DATABASE_URL, save and exit

touch ~/repositories/Registeration-Bot/tmp/restart.txt
```

---

## ✅ Verify Fix

```bash
curl https://yourdomain.com
```

Should show: `"database_ready": true`

---

## 📝 What Changed in main.py

The app now:
- ✅ Starts even if database is not ready
- ✅ Attempts database init on first request
- ✅ Shows clear error messages
- ✅ No more cleanup errors
- ✅ Handles "unclosed session" warnings better

**Upload the updated `main.py` and restart!**
