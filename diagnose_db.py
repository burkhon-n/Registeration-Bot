#!/usr/bin/env python3
"""
Database Connection Diagnostic Script
Run this on your server to diagnose DATABASE_URL issues
"""
import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("DATABASE CONNECTION DIAGNOSTIC")
print("=" * 60)
print()

# Load environment
load_dotenv()

# Check if .env exists
if not os.path.exists('.env'):
    print("❌ ERROR: .env file not found!")
    print("   Create a .env file with DATABASE_URL")
    sys.exit(1)
else:
    print("✅ .env file found")

# Get DATABASE_URL
db_url = os.getenv('DATABASE_URL')

if not db_url:
    print("❌ ERROR: DATABASE_URL not set in .env")
    print("   Add: DATABASE_URL=postgresql://user:pass@host:port/dbname")
    sys.exit(1)
else:
    print(f"✅ DATABASE_URL is set")

# Parse DATABASE_URL (hide password)
try:
    from urllib.parse import urlparse
    parsed = urlparse(db_url)
    
    print()
    print("DATABASE_URL Details:")
    print(f"  Protocol: {parsed.scheme}")
    print(f"  Username: {parsed.username}")
    print(f"  Password: {'*' * len(parsed.password) if parsed.password else 'NOT SET'}")
    print(f"  Hostname: {parsed.hostname}")
    print(f"  Port: {parsed.port}")
    print(f"  Database: {parsed.path.lstrip('/')}")
    print()
    
    # Check for common issues
    issues = []
    
    if parsed.scheme not in ['postgresql', 'postgres']:
        issues.append(f"⚠️  Protocol should be 'postgresql' not '{parsed.scheme}'")
    
    if not parsed.hostname:
        issues.append("❌ Hostname is missing!")
    elif parsed.hostname not in ['localhost', '127.0.0.1']:
        issues.append(f"⚠️  Using remote host: {parsed.hostname}")
        issues.append("   Make sure this hostname is resolvable and accessible")
    
    if not parsed.port:
        issues.append("⚠️  Port not specified (will use default 5432)")
    
    if not parsed.path or parsed.path == '/':
        issues.append("❌ Database name is missing!")
    
    if not parsed.username:
        issues.append("❌ Username is missing!")
    
    if not parsed.password:
        issues.append("⚠️  Password is missing!")
    
    if issues:
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        print()
    else:
        print("✅ URL format looks correct")
        print()
    
except Exception as e:
    print(f"❌ Error parsing DATABASE_URL: {e}")
    print()

# Test hostname resolution
print("Testing hostname resolution...")
try:
    import socket
    from urllib.parse import urlparse
    parsed = urlparse(db_url)
    
    if parsed.hostname:
        try:
            ip = socket.gethostbyname(parsed.hostname)
            print(f"✅ Hostname '{parsed.hostname}' resolves to: {ip}")
        except socket.gaierror:
            print(f"❌ CANNOT RESOLVE HOSTNAME: '{parsed.hostname}'")
            print(f"   This is your main problem!")
            print()
            print("   Common fixes:")
            print("   1. Use 'localhost' instead of a custom hostname")
            print("   2. Use '127.0.0.1' for local database")
            print("   3. Check if hostname is correct for cPanel")
            print()
    else:
        print("❌ No hostname to test")
except Exception as e:
    print(f"❌ Error testing hostname: {e}")

print()
print("-" * 60)

# Try to connect
print("Attempting database connection...")
try:
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError
    
    # Convert to psycopg3 format
    test_url = db_url
    if test_url.startswith('postgresql://'):
        test_url = test_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    elif test_url.startswith('postgres://'):
        test_url = test_url.replace('postgres://', 'postgresql+psycopg://', 1)
    
    engine = create_engine(test_url, echo=False)
    
    # Try to connect
    with engine.connect() as conn:
        result = conn.execute("SELECT version()")
        version = result.fetchone()[0]
        print("✅ DATABASE CONNECTION SUCCESSFUL!")
        print(f"   PostgreSQL Version: {version[:50]}...")
        print()
        print("🎉 Your DATABASE_URL is working correctly!")
        print("   The application should work now.")
        
except OperationalError as e:
    error_msg = str(e)
    print(f"❌ CONNECTION FAILED: {error_msg}")
    print()
    
    if "Name or service not known" in error_msg:
        print("ROOT CAUSE: Hostname cannot be resolved")
        print()
        print("SOLUTION:")
        print("  Update your DATABASE_URL in .env file:")
        print()
        print("  For cPanel with local PostgreSQL:")
        print(f"  DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/YOUR_DATABASE")
        print()
        
    elif "password authentication failed" in error_msg:
        print("ROOT CAUSE: Wrong username or password")
        print()
        print("SOLUTION:")
        print("  Check your PostgreSQL username and password in cPanel")
        print("  Update DATABASE_URL with correct credentials")
        
    elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
        print("ROOT CAUSE: Database does not exist")
        print()
        print("SOLUTION:")
        print("  Create the database using:")
        print(f"  - cPanel → PostgreSQL Databases → Create Database")
        print("  - Or: createdb -U username database_name")
        
    elif "Connection refused" in error_msg:
        print("ROOT CAUSE: PostgreSQL server is not running or not accessible")
        print()
        print("SOLUTION:")
        print("  - Check if PostgreSQL is running")
        print("  - Verify firewall settings")
        print("  - Check if port is correct (usually 5432)")
    
    else:
        print("Check the error message above for clues")
        
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print()
print("=" * 60)
print()
print("RECOMMENDED DATABASE_URL FORMAT FOR CPANEL:")
print()
print("DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/USERNAME_DBNAME")
print()
print("Example:")
print("DATABASE_URL=postgresql://bagriken:mypassword@localhost:5432/bagriken_registration_bot")
print()
print("=" * 60)
