# 🔍 Diagnose Database Connection Issue

Your app is now starting correctly, but the database connection is failing with:
```
[Errno -2] Name or service not known
```

This means the **hostname in your DATABASE_URL cannot be resolved**.

---

## 🚀 Quick Diagnosis

### Run this on your server:

```bash
cd ~/repositories/Registeration-Bot
source ~/virtualenv/repositories/Registeration-Bot/3.13/bin/activate
python diagnose_db.py
```

This script will:
- ✅ Check if .env file exists
- ✅ Validate DATABASE_URL format
- ✅ Test hostname resolution
- ✅ Attempt database connection
- ✅ Show you exactly what's wrong
- ✅ Suggest the fix

---

## 🔧 Most Likely Fix

Your DATABASE_URL probably has a hostname that doesn't exist. 

### Check your current DATABASE_URL:
```bash
cd ~/repositories/Registeration-Bot
cat .env | grep DATABASE_URL
```

### It should look like this for cPanel:
```env
DATABASE_URL=postgresql://bagriken:YOUR_PASSWORD@localhost:5432/bagriken_registration_bot
```

**Key points:**
- Use `localhost` (not a custom hostname)
- Use your actual database password
- Database name format: `username_dbname` (for cPanel)

---

## 📋 Common Issues & Fixes

### Issue 1: Using a non-existent hostname
```env
# ❌ Wrong:
DATABASE_URL=postgresql://user:pass@my-db-server:5432/db

# ✅ Correct:
DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

### Issue 2: Wrong protocol
```env
# ❌ Wrong:
DATABASE_URL=postgres://user:pass@localhost:5432/db

# ✅ Correct:
DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

### Issue 3: Database doesn't exist
Create it in cPanel:
- Go to: **PostgreSQL Databases**
- Click: **Create Database**
- Name it: `bagriken_registration_bot` (or similar)

### Issue 4: Wrong credentials
Get the correct credentials from cPanel:
- **PostgreSQL Databases** section
- Check username (usually same as cPanel username)
- Check/reset database password if needed

---

## ✅ After Fixing

1. Update `.env` file with correct DATABASE_URL
2. Restart the application:
   ```bash
   cd ~/repositories/Registeration-Bot
   touch tmp/restart.txt
   ```
3. Test:
   ```bash
   curl https://yourdomain.com
   # Should show: "database_ready": true
   ```

---

## 📞 Need Help?

Run the diagnostic script and share the output:
```bash
python diagnose_db.py
```

This will tell you exactly what's wrong with your DATABASE_URL!
