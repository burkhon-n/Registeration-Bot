# Admin Feature - Quick Setup

## 🚀 Quick Start

### Step 1: Get Your Telegram User ID
Message [@userinfobot](https://t.me/userinfobot) on Telegram to get your ID.

### Step 2: Add to .env File
```bash
ADMIN_IDS=YOUR_TELEGRAM_USER_ID_HERE
```

Example:
```bash
ADMIN_IDS=123456789
```

For multiple admins:
```bash
ADMIN_IDS=123456789,987654321
```

### Step 3: Install New Dependency
```bash
.venv/bin/pip install openpyxl==3.1.2
```

### Step 4: Restart Bot
```bash
.venv/bin/python run.py
```

## 📊 How to Use

1. Send `/start` to your bot
2. You'll see a special admin button: **📊 Ma'lumotlarni yuklab olish (Admin)**
3. Click it to download an Excel file with all data

## 📁 What You Get

An Excel file with 3 sheets:
1. **Foydalanuvchilar** - All registered users with complete details
2. **Loyihalar** - All submitted projects with participant info
3. **Statistika** - Summary statistics and breakdowns

## ✨ Features

- ✅ Clean, professional formatting
- ✅ Color-coded headers (blue background, white text)
- ✅ Auto-sized columns for easy reading
- ✅ Complete statistics by region and project type
- ✅ Timestamped file names
- ✅ Works for multiple admins
- ✅ Secure - only admins can access

## 🔒 Security Note

Only Telegram users listed in ADMIN_IDS can:
- See the admin button
- Export data
- Non-admins will get an error message

---

For detailed documentation, see ADMIN_GUIDE.md
