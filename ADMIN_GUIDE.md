# Admin Guide

## Admin Configuration

### Setting Up Admin Access

1. **Get Your Telegram User ID:**
   - Start a chat with [@userinfobot](https://t.me/userinfobot)
   - It will reply with your Telegram user ID (e.g., 123456789)

2. **Add Admin ID to .env:**
   ```bash
   # For single admin
   ADMIN_IDS=123456789
   
   # For multiple admins (comma-separated)
   ADMIN_IDS=123456789,987654321,555444333
   ```

3. **Restart the bot** after updating the .env file

## Admin Features

### Exporting Data

When an admin sends `/start` command, they will see an additional button:
- **📊 Ma'lumotlarni yuklab olish (Admin)** - Download all data as Excel

### Excel File Structure

The exported Excel file contains 3 sheets:

#### Sheet 1: Foydalanuvchilar (Users)
Contains all registered users with:
- Sequential number
- Telegram ID
- Full name
- Region (Viloyat)
- District (Tuman)
- Neighborhood (Mahalla)
- Workplace
- Birth date
- Passport
- Phone number
- Number of submitted projects

#### Sheet 2: Loyihalar (Projects)
Contains all submitted projects with:
- Sequential number
- Participant name
- Telegram ID
- Project type
- Project URL (link to channel message)
- Region
- District
- Phone number

#### Sheet 3: Statistika (Statistics)
Contains:
- Total registered users
- Total submitted projects
- Breakdown by regions
- Breakdown by project types

### Features

✅ **Easy to read** - Clean formatting with headers and proper column widths
✅ **Color-coded headers** - Blue background with white text
✅ **Center-aligned data** - All data is centered for easy reading
✅ **Auto-sized columns** - Columns adjust to content width
✅ **Comprehensive stats** - Complete overview of all data
✅ **Timestamped** - File name includes export date

### Security

- Only users listed in `ADMIN_IDS` can access admin features
- Non-admin users will see an error message if they try to access admin functions
- All admin actions are logged

### Usage

1. Admin sends `/start`
2. Clicks "📊 Ma'lumotlarni yuklab olish (Admin)"
3. Bot shows "⏳ Ma'lumotlar tayyorlanmoqda..." message
4. Bot generates Excel file with all data
5. Bot sends the file with summary statistics
6. File is named with current date: `Tanlov_malumotlari_11_10_2025.xlsx`

### Troubleshooting

**Issue:** Admin button not showing
- **Solution:** Make sure your Telegram ID is correctly added to ADMIN_IDS in .env
- **Solution:** Restart the bot after updating .env

**Issue:** Error when exporting data
- **Solution:** Check database connection
- **Solution:** Check bot logs for detailed error message
- **Solution:** Ensure openpyxl is installed: `pip install openpyxl==3.1.2`

**Issue:** Excel file is empty
- **Solution:** Check if there is any data in the database
- **Solution:** Verify regions.json file exists and is properly formatted
