#!/bin/bash

# Complete setup script for cPanel deployment
# Run this script on your cPanel server after uploading files

echo "=========================================="
echo "Setting up Registration Bot on cPanel"
echo "=========================================="
echo ""

# Get the current directory
PROJECT_DIR=$(pwd)
echo "Project directory: $PROJECT_DIR"
echo ""

# Step 1: Fix all permissions
echo "Step 1: Fixing file permissions..."
chmod 755 "$PROJECT_DIR"
find "$PROJECT_DIR" -type d -exec chmod 755 {} \;
find "$PROJECT_DIR" -type f -exec chmod 644 {} \;
chmod 755 "$PROJECT_DIR/passenger_wsgi.py"
chmod 755 "$PROJECT_DIR/setup.sh"
chmod 755 "$PROJECT_DIR/run.py"
echo "✓ Permissions fixed"
echo ""

# Step 2: Check Python version
echo "Step 2: Checking Python version..."
PYTHON_CMD=$(which python3.13 || which python3.11 || which python3.10 || which python3)
echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Step 3: Create virtual environment if it doesn't exist
if [ ! -d "$HOME/virtualenv/repositories/Registeration-Bot/3.13" ]; then
    echo "Step 3: Creating virtual environment..."
    mkdir -p "$HOME/virtualenv/repositories/Registeration-Bot"
    $PYTHON_CMD -m venv "$HOME/virtualenv/repositories/Registeration-Bot/3.13"
    echo "✓ Virtual environment created"
else
    echo "Step 3: Virtual environment already exists"
fi
echo ""

# Step 4: Activate virtual environment and install dependencies
echo "Step 4: Installing dependencies..."
source "$HOME/virtualenv/repositories/Registeration-Bot/3.13/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Step 5: Check database configuration
echo "Step 5: Checking configuration..."
if [ -f .env ]; then
    echo "✓ .env file found"
else
    echo "⚠ Warning: .env file not found. Please create it with your configuration."
fi
echo ""

# Step 6: Restart Passenger
echo "Step 6: Restarting application..."
mkdir -p tmp
touch tmp/restart.txt
echo "✓ Application restart triggered"
echo ""

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure your .env file is configured with correct database credentials"
echo "2. Check the application at your domain"
echo "3. Monitor logs if there are any issues"
echo ""
