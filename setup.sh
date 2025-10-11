#!/bin/bash

# Setup script for Registration Bot

echo "🤖 Registration Bot Setup"
echo "========================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cat > .env << 'EOF'
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://yourdomain.com

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/registration_bot
EOF
    echo "✅ .env file created. Please edit it with your actual values."
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL is installed"
    
    # Try to connect
    if psql -U postgres -c '\q' 2>/dev/null; then
        echo "✅ PostgreSQL is running"
    else
        echo "⚠️  PostgreSQL is installed but may not be running"
        echo "   Start it with: brew services start postgresql@16"
    fi
else
    echo "❌ PostgreSQL not found. Install it with:"
    echo "   brew install postgresql@16"
fi
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create database
echo "🗄️  Setting up database..."
read -p "Do you want to create the database now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter database name [registration_bot]: " db_name
    db_name=${db_name:-registration_bot}
    
    read -p "Enter PostgreSQL username [postgres]: " db_user
    db_user=${db_user:-postgres}
    
    if psql -U "$db_user" -c "CREATE DATABASE $db_name;" 2>/dev/null; then
        echo "✅ Database '$db_name' created successfully"
    else
        echo "⚠️  Database might already exist or check your PostgreSQL credentials"
    fi
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your bot token and database credentials"
echo "2. If using ngrok for development: ngrok http 8000"
echo "3. Copy the ngrok URL to WEBHOOK_URL in .env"
echo "4. Run the bot: python3 main.py"
echo ""
