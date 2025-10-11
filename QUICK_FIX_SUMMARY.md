# ⚡ Quick Reference - What Changed

## The Core Issue
FastAPI's `@app.on_event("startup")` and `@app.on_event("shutdown")` **DON'T WORK** with WSGI/Passenger!

## The Fix

### Before (Broken with WSGI):
```python
@app.on_event("startup")
async def on_startup():
    init_db()
    await bot.set_webhook(...)
```

### After (Works with WSGI):
```python
def initialize_app():
    init_db()

# In passenger_wsgi.py:
from main import app, initialize_app
initialize_app()  # Called directly on load
application = ASGIMiddleware(app)
```

---

## Files Changed

1. **main.py**
   - ✅ Added `initialize_app()` - called by passenger_wsgi.py
   - ✅ Added `cleanup_app()` with `atexit.register()`
   - ✅ Removed `@app.on_event()` decorators
   - ✅ Lazy webhook setup on first request

2. **passenger_wsgi.py**
   - ✅ Imports and calls `initialize_app()`
   - ✅ Uses `ASGIMiddleware` (not WSGIMiddleware)

3. **database.py**
   - ✅ Auto-converts `postgresql://` to `postgresql+psycopg://`

4. **requirements.txt**
   - ✅ Updated `aiohttp` to `>=3.10.0`

---

## Deploy Commands

```bash
cd ~/repositories/Registeration-Bot
git pull  # or upload files manually
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
touch tmp/restart.txt
```

---

## Verify

```bash
# Check logs
tail -50 ~/logs/passenger.log

# Should see: "Database initialized successfully"
# Should NOT see: errors about psycopg2 or WSGIMiddleware

# Test
curl https://yourdomain.com
# Should return: {"status":"running",...}
```

---

## All Fixed Issues

1. ✅ WSGIMiddleware TypeError
2. ✅ psycopg2 not found
3. ✅ aiohttp build error
4. ✅ Startup events not working
5. ✅ Shutdown events not working
6. ✅ Unclosed sessions
7. ✅ WSGI compatibility

**Status: Production Ready! 🚀**
