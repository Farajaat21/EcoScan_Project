#!/bin/bash

echo "🌳 Starting EcoScan Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r backend/requirements.txt
fi

# Activate virtual environment
source venv/bin/activate

# Start backend server
echo "Starting backend server on http://localhost:8000..."
python test_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "Starting frontend server on http://localhost:3000..."
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "🚀 EcoScan is now running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "🌟 New Features Available:"
echo "   📊 Solution Page: http://localhost:3000/solution.html"
echo "   🔍 Product Search: http://localhost:3000/search.html"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait

# Clean up background processes
echo "Stopping servers..."
kill $BACKEND_PID 2>/dev/null
kill $FRONTEND_PID 2>/dev/null
echo "Servers stopped."
