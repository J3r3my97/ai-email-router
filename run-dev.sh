#!/bin/bash

# AI Email Router Development Setup Script

echo "🚀 Starting AI Email Router development environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying .env.example to .env"
    cp .env.example .env
    echo "📝 Please edit .env file with your actual API keys and configuration"
    echo "   Required: SENDGRID_API_KEY, OPENAI_API_KEY, DOMAIN, SECRET_KEY"
    read -p "Press Enter after you've configured your .env file..."
fi

# Start backend
echo "🔧 Starting Python backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

# Start backend in background
python main.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"

cd ..

# Start frontend
echo "🎨 Starting Next.js frontend..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

cd ..

echo ""
echo "🎉 Development environment is ready!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the development servers:"
echo "kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap 'echo "🛑 Stopping development servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT
wait