#!/bin/bash

echo "🚀 Setting up CV Matchy-Matchy..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

echo "✅ Python 3 and Node.js are installed"

# Setup backend
echo "📦 Setting up backend..."
cd backend
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cd ..

# Setup frontend
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get a free API key from https://huggingface.co/settings/tokens"
echo "2. Create a .env file in the backend directory with:"
echo "   HUGGINGFACE_API_KEY=your_api_key_here"
echo "3. Start the backend: cd backend && python3 app.py"
echo "4. Start the frontend: cd frontend && npm start"
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo "🎉 Happy CV analyzing!" 