# Admin Command: /clear_results

## 🎯 Purpose

Clear all data from the database including users, addresses, and projects. This is useful for:
- Resetting the bot for a new competition period
- Testing purposes
- Removing all data after exporting

## 🔐 Security

- **Admin Only**: Only users in `config.ADMIN_IDS` can use this command
- **Confirmation Required**: Requires explicit confirmation before deletion
- **Audit Trail**: All actions logged with WARNING/CRITICAL levels
- **Non-reversible**: Cannot undo once confirmed

## 📝 Usage

### Step 1: Send Command
```
/clear_results
```

### Step 2: Confirm
Bot will ask for confirmation:
```
⚠️ OGOHLANTIRISH!

Siz barcha ma'lumotlarni o'chirmoqchisiz:
• Barcha foydalanuvchilar
• Barcha manzillar
• Barcha loyihalar

Bu amalni qaytarib bo'lmaydi!

Davom etishni xohlaysizmi?
```

Options:
- ✅ **Ha, barcha ma'lumotlarni o'chirish** - Confirms deletion
- ❌ **Yo'q, bekor qilish** - Cancels operation

### Step 3: Deletion
If confirmed, bot will:
1. Show "⏳ Ma'lumotlar o'chirilmoqda..."
2. Delete all records
3. Show success message with statistics

## ✅ Success Response

```
✅ Barcha ma'lumotlar o'chirildi!

📊 O'chirilgan ma'lumotlar:
• Foydalanuvchilar: 150
• Manzillar: 150
• Loyihalar: 220

Database endi bo'sh.
```

## ❌ Cancel Response

```
❌ Bekor qilindi. Hech qanday ma'lumot o'chirilmadi.
```

## 🗄️ What Gets Deleted

1. **All Projects** (`projects` table)
   - Project submissions
   - Project URLs
   - Project types

2. **All Users** (`users` table)
   - User registrations
   - Personal information
   - Telegram IDs

3. **All Addresses** (`addresses` table)
   - Region information
   - District information
   - Neighborhood information

## ⚠️ Important Notes

### Before Deletion
✅ **Recommended**: Export data first using "📊 Ma'lumotlarni yuklab olish"

### Deletion Order
The system deletes in this order (to respect foreign key constraints):
1. Projects (references users)
2. Users (references addresses)
3. Addresses (no dependencies)

### Cannot Delete
This command does NOT delete:
- Bot configuration
- Admin IDs
- Region/district data (from regions.json)
- Bot settings

## 📊 Logging

All actions are logged with appropriate levels:

### Attempt
```log
WARNING - bot - Admin 123456 initiated database clear request
```

### Confirmation
```log
CRITICAL - bot - Admin 123456 confirmed database clear - DELETING ALL DATA
WARNING - bot - Deleting 150 users, 150 addresses, 220 projects
```

### Success
```log
CRITICAL - bot - Database cleared successfully by admin 123456: 150 users, 150 addresses, 220 projects deleted
```

### Unauthorized Attempt
```log
WARNING - bot - Non-admin user 999999 attempted to clear database
```

### Error
```log
ERROR - bot - Error clearing database: <error message>
```

## 🔍 Verification

After clearing, verify:

### Check Database
```bash
cd ~/repositories/Registeration-Bot
source ~/virtualenv/repositories/Registeration-Bot/3.13/bin/activate
python -c "
from database import SessionLocal
from models.User import User
from models.Project import Project
from models.Address import Address

db = SessionLocal()
print(f'Users: {db.query(User).count()}')
print(f'Projects: {db.query(Project).count()}')
print(f'Addresses: {db.query(Address).count()}')
db.close()
"
```

Expected output:
```
Users: 0
Projects: 0
Addresses: 0
```

### Check Logs
```bash
grep "Database cleared successfully" logs/app.log
```

## 🚫 Error Handling

If an error occurs:
1. Transaction is rolled back
2. No data is deleted
3. Error message shown to admin
4. Full error logged with stack trace

## 💡 Best Practices

### 1. Export Before Clearing
```
1. Send: 📊 Ma'lumotlarni yuklab olish (Admin)
2. Download Excel file
3. Verify data is saved
4. Then send: /clear_results
```

### 2. Document Deletion
Keep a record:
- Date of deletion
- Who performed deletion
- Number of records deleted
- Reason for deletion

### 3. Test First
On development/test environment:
```bash
# Test the command
# Verify it works
# Then use in production
```

### 4. Backup Database
Before major deletions:
```bash
# On server
pg_dump bagriken_registration > backup_$(date +%Y%m%d).sql
```

## 🎯 Use Cases

### End of Competition
```
1. Export final results
2. Announce winners
3. Clear database for next period
4. Ready for new registrations
```

### Testing
```
1. Add test data
2. Test bot functionality
3. Clear test data
4. Ready for production
```

### Data Privacy
```
1. Export required data
2. Process/anonymize externally
3. Clear personal information
4. Compliance maintained
```

## 📞 Support

If deletion fails:
1. Check logs for error details
2. Verify database connection
3. Check foreign key constraints
4. Manual cleanup if needed:
   ```sql
   DELETE FROM projects;
   DELETE FROM users;
   DELETE FROM addresses;
   ```

## ⚡ Quick Reference

| Action | Command | Access |
|--------|---------|--------|
| Clear database | `/clear_results` | Admin only |
| Confirm deletion | Click "✅ Ha, barcha ma'lumotlarni o'chirish" | After /clear_results |
| Cancel deletion | Click "❌ Yo'q, bekor qilish" | After /clear_results |
| Check if cleared | Export data - should be empty | Admin |

---

**Added**: October 13, 2025  
**Version**: 1.0  
**Status**: ✅ Implemented and Tested  
**Safety Level**: 🔴 CRITICAL - Requires confirmation
