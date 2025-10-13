# Logging Implementation Guide

This document describes the comprehensive logging system implemented for the Registration Bot.

## Overview

The application now includes production-grade logging with:
- File-based rotating logs
- Separate error logs
- Detailed request/response logging
- User activity tracking
- Database operation logging
- Admin action logging

## Log Configuration

### Main Application (`main.py`)

**Location**: `logs/app.log` and `logs/error.log`

**Configuration**:
- **Format**: `%(asctime)s - %(levelname)s - %(name)s - %(message)s`
- **Date Format**: `%Y-%m-%d %H:%M:%S`
- **Max Size**: 10MB per file
- **Backup Count**: 5 files
- **Encoding**: UTF-8

**Handlers**:
1. **RotatingFileHandler (app.log)**: Logs all levels (INFO and above)
2. **RotatingFileHandler (error.log)**: Logs only ERROR level and above
3. **StreamHandler**: Console output for development

## What Gets Logged

### 1. Web Application Endpoints (`main.py`)

#### Root Endpoint (`/`)
- Access timestamp
- Database initialization attempts
- Webhook setup status
- Response details

#### Webhook Endpoint (`/webhook`)
- Incoming update IDs
- User IDs and chat IDs
- Message content (first 50 chars)
- Processing success/failure
- Full exception traces on errors

#### Health Check (`/health`)
- Access frequency tracking

#### Webhook Info (`/webhook-info`)
- Webhook status queries
- Current webhook configuration

### 2. Bot Handlers (`bot.py`)

#### User Authentication
- `/start` command usage
- Admin access grants
- User identification (ID and username)

#### Registration Flow
- Registration button clicks
- Existing user checks
- New registration flow initiations
- User data confirmation
- Profile updates

#### Project Submissions
- File uploads (type and user)
- Project type selection
- Submission success/failure
- Project URLs generated
- Channel forwarding status

#### Admin Actions
- Admin function access attempts
- Unauthorized access attempts
- Data export operations
- Export statistics (user count, project count)

### 3. Database Operations (`database.py`)

- Database URL conversions (postgresql:// → postgresql+psycopg://)
- Engine creation
- Connection pool configuration
- Table creation
- Database errors with stack traces

## Log Levels Used

| Level | Usage |
|-------|-------|
| **INFO** | Normal operations, user actions, successful operations |
| **WARNING** | Potential issues, unauthorized access attempts |
| **ERROR** | Errors requiring attention, exceptions |

## Example Log Entries

### Successful User Registration
```
2024-01-15 10:30:45,123 - INFO - bot - User 123456 (@username) started the bot with /start command
2024-01-15 10:30:46,234 - INFO - bot - User 123456 clicked registration button
2024-01-15 10:30:50,567 - INFO - bot - Starting new registration flow for user 123456
2024-01-15 10:35:12,890 - INFO - bot - User 123456 data updated successfully
```

### Webhook Processing
```
2024-01-15 10:30:45,123 - INFO - main - Received webhook update: update_id=123456789
2024-01-15 10:30:45,234 - INFO - main - Message from user 123456 in chat 123456: Hello bot
2024-01-15 10:30:45,456 - INFO - main - Webhook processed successfully
```

### Project Submission
```
2024-01-15 11:00:00,123 - INFO - bot - Received project file (photo) from user 123456
2024-01-15 11:00:02,456 - INFO - bot - Project saved successfully for user 123456: type=article, url=https://t.me/c/123456/789
```

### Admin Export
```
2024-01-15 12:00:00,123 - INFO - bot - Admin 789012 initiated data export
2024-01-15 12:00:05,456 - INFO - bot - Admin 789012 exported data successfully: 150 users, 220 projects
```

### Error Example
```
2024-01-15 10:30:45,123 - ERROR - main - Error processing webhook: Connection timeout
Traceback (most recent call last):
  File "main.py", line 95, in webhook
    ...
ConnectionError: Connection timeout
```

### Unauthorized Access
```
2024-01-15 13:00:00,123 - WARNING - bot - Non-admin user 999999 attempted to access admin export function
```

## Monitoring Tips

### Real-time Monitoring
```bash
# Follow all logs
tail -f logs/app.log

# Follow only errors
tail -f logs/error.log

# Follow both simultaneously
tail -f logs/app.log logs/error.log
```

### Analyzing Logs
```bash
# Count total requests today
grep "$(date +%Y-%m-%d)" logs/app.log | wc -l

# Find all errors
grep "ERROR" logs/app.log

# Find specific user activity
grep "user 123456" logs/app.log

# Find project submissions
grep "Project saved successfully" logs/app.log

# Find admin actions
grep "Admin" logs/app.log
```

### Log Rotation Status
```bash
# Check log file sizes
ls -lh logs/

# View rotation history
ls -lt logs/*.log*
```

## Troubleshooting

### Logs Not Being Created
1. Check directory permissions:
   ```bash
   chmod 755 logs/
   ```
2. Verify application has write access
3. Check disk space

### Too Many Log Files
- Log rotation keeps only 5 backups automatically
- Manually clean old logs if needed:
  ```bash
  rm logs/*.log.[5-9]
  ```

### High Log Volume
- Logs rotate at 10MB automatically
- Consider increasing `maxBytes` in configuration if needed
- Adjust `backupCount` for more/fewer backup files

## Production Deployment

### cPanel Access
1. **SSH Access**:
   ```bash
   ssh bagriken@bagrikenglik.uz
   cd ~/repositories/Registeration-Bot/logs
   tail -f app.log
   ```

2. **File Manager**:
   - Navigate to `/home/bagriken/repositories/Registeration-Bot/logs/`
   - Download logs as needed

### Log Retention
- Current configuration retains ~50MB of logs (10MB × 5 backups)
- Adjust `backupCount` in `main.py` if different retention needed

### Security
- Logs directory is excluded from git (`.gitignore`)
- Sensitive data (passwords, tokens) not logged
- Only user IDs and non-sensitive data logged

## Future Enhancements

Potential improvements:
1. Log aggregation service integration (e.g., Sentry, Loggly)
2. Daily log summaries via email
3. Performance metrics logging
4. Structured JSON logging for better parsing
5. Log level configuration via environment variables
