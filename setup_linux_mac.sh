#!/bin/bash

echo "========================================"
echo "Chemical Equipment Visualizer Setup"
echo "FOSSEE Internship 2026"
echo "========================================"
echo ""

echo "[1/4] Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
deactivate
echo "Backend setup complete!"
echo ""

echo "[2/4] Setting up Web Frontend..."
cd ../frontend-web
npm install
echo "Web frontend setup complete!"
echo ""

echo "[3/4] Setting up Desktop Frontend..."
cd ../frontend-desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
echo "Desktop frontend setup complete!"
echo ""

echo "[4/4] Setup Complete!"
echo ""
echo "========================================"
echo "Next Steps:"
echo "========================================"
echo "1. Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Start Web Frontend (new terminal):"
echo "   cd frontend-web"
echo "   npm start"
echo ""
echo "3. Start Desktop App (new terminal):"
echo "   cd frontend-desktop"
echo "   source venv/bin/activate"
echo "   python main.py"
echo "========================================"
