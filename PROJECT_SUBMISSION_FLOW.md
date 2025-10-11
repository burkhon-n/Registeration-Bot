# Project Submission Flow - Implementation Summary

## 🎯 What Changed

The bot now has a complete project submission system where files are forwarded to a Telegram channel instead of just collecting URLs.

## 📋 New Flow

### 1. Personal Data Collection (Unchanged)
- Full name → Region → District → **Mahalla (NEW)** → Workplace → Birth Date → Passport → Phone

### 2. Data Confirmation (NEW)
- User reviews all entered data
- Can edit any specific field (Name, Address, Workplace, Date, Passport, Phone)
- After editing, returns to confirmation screen

### 3. Project Submission (COMPLETELY NEW)
- User selects project type from 6 categories
- User uploads project file (document, photo, audio, video)
- Bot forwards file to designated channel
- Bot replies to forwarded message with user data
- Bot saves channel message URL as project_url

### 4. Multiple Submissions
- After successful submission, user can:
  - Submit another project (➕ Yana loyiha yuborish)
  - Return to home (🏠 Bosh sahifa)

## 🗂️ Database Structure

### Updated Models:
```
User (users table)
├── telegram_id
├── full_name
├── address_id → Address
├── workplace
├── birth_date
├── passport_series
└── phone_number

Address (addresses table)
├── region_id
├── district_id
└── neighborhood (mahalla)

Project (projects table)
├── user_id → User
├── type (essay/poem/song/art/craft/video)
└── project_url (Telegram channel message URL)
```

## ⚙️ Configuration Changes

### config.py - Added:
```python
CHANNEL_ID = "@your_channel"  # Channel for project submissions

PROJECT_TYPES = {
    'essay': {'title': "✍️ Maqola yoki esse", 'file_types': "doc, docx, pdf"},
    'poem': {'title': "🎤 She'r yoki monolog", 'file_types': "doc, docx, pdf"},
    'song': {'title': "🎶 Qo'shiq yoki musiqiy chiqish", 'file_types': "mp3, wav"},
    'art': {'title': "🎨 Rassomchilik ishi", 'file_types': "jpg, png, gif"},
    'craft': {'title': "🧵 Hunarmandchilik namunasi", 'file_types': "jpg, png, pdf"},
    'video': {'title': "🎥 Video-rolik yoki kontent", 'file_types': "mp4, avi"}
}
```

### .env - Add this line:
```env
CHANNEL_ID=@your_channel_username
```

## 🔧 Bot States Updated

```python
class RegistrationStates:
    full_name
    region
    district
    mahalla          # NEW
    workplace
    birth_date
    passport_series
    phone_number
    confirmation     # NEW
    project_type     # NEW (replaced project_url)
    project_file     # NEW (replaced project_url)
```

## 📝 Key Features Implemented

### 1. Mahalla Field
- Asked after district selection
- Saved to Address.neighborhood field
- Shown in confirmation

### 2. Passport Case-Insensitive
- Accepts: `aa1234567` or `AA1234567`
- Auto-converts to uppercase before saving
- Pattern: 2 letters + 7 digits

### 3. Date Validation
- Format: DD.MM.YYYY only
- Validates real dates (no 32.13.2020)
- Shows error if invalid

### 4. Data Confirmation Screen
- Shows all collected data
- Options: "✅ Ha, to'g'ri" or "✏️ Tahrirlash"
- Edit menu with 6 options + back button
- After editing any field, returns to confirmation

### 5. Project Submission
- Select from 6 project types
- Upload file (any media type)
- Bot forwards to channel
- Bot replies with user data formatted nicely
- Saves channel message URL
- User can submit multiple projects

### 6. Channel Integration
- Forwards project file
- Posts user data as reply
- URL format: `https://t.me/channel_username/message_id`
- All submissions in one channel for easy management

## 🎬 User Experience Example

```
1. User: /start
2. Bot: Welcome message
3. User: Click "Ro'yxatdan o'tish"
4. Bot: Enter your name
5. User: Aliyev Vali
6. Bot: Select region [buttons]
7. User: Toshkent shahri
8. Bot: Select district [buttons]
9. User: Chilonzor tumani
10. Bot: Enter mahalla
11. User: Yangi hayot
12. Bot: Enter workplace
13. User: Toshkent davlat universiteti
14. Bot: Enter birth date (DD.MM.YYYY)
15. User: 01.01.2000
16. Bot: Enter passport (AA1234567)
17. User: ad1654502 (lowercase accepted)
18. Bot: Share phone [contact button]
19. User: [shares contact]
20. Bot: Review data [shows all info] - Ha to'g'ri / Tahrirlash
21. User: ✅ Ha, to'g'ri
22. Bot: Select project type [6 buttons]
23. User: ✍️ Maqola yoki esse
24. Bot: Upload your file (doc, docx, pdf)
25. User: [uploads essay.pdf]
26. Bot: ✅ Thanks! [Submit another / Home]
```

## 🚀 Setup Steps for You

1. **Update .env file:**
   ```env
   CHANNEL_ID=@your_channel_username
   ```

2. **Make bot admin of the channel:**
   - Add bot to channel
   - Give admin rights (at least post messages)

3. **Test the flow:**
   - Go through registration
   - Upload a test file
   - Check if it appears in channel
   - Verify user data is posted as reply

4. **Restart the bot:**
   ```bash
   # Bot will auto-reload if using uvicorn with reload
   # Or manually restart
   ```

## ✨ Benefits

✅ All projects in one channel (organized)
✅ User data attached to each project
✅ Easy review process
✅ Multiple submissions per user
✅ Professional workflow
✅ Message URLs for tracking
✅ No need for external file storage

## 🔍 What to Monitor

- Check channel receives files correctly
- Verify user data formatting
- Test different file types
- Ensure URLs are generated correctly
- Monitor database for project records

---

**Status: ✅ Ready to test!**

The bot will auto-reload and the new flow is active. Just add your CHANNEL_ID to .env and you're good to go! 🚀
