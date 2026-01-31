# 🚀 QUICK START GUIDE

## For Windows Users

### Automated Setup
```cmd
setup_windows.bat
```

### Manual Setup
```cmd
:: Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

:: Web Frontend (new terminal)
cd frontend-web
npm install
npm start

:: Desktop App (new terminal)
cd frontend-desktop
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## For Linux/Mac Users

### Automated Setup
```bash
chmod +x setup_linux_mac.sh
./setup_linux_mac.sh
```

### Manual Setup
```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Web Frontend (new terminal)
cd frontend-web
npm install
npm start

# Desktop App (new terminal)
cd frontend-desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 📍 Access Points

- **Backend API:** http://localhost:8000/api/
- **Web App:** http://localhost:3000
- **Desktop App:** Launches in separate window
- **Admin Panel:** http://localhost:8000/admin/

---

## 🧪 Test with Sample Data

1. Open web app or desktop app
2. Click "Select CSV File" / "Choose File"
3. Select `sample_equipment_data.csv` from project root
4. Click "Upload & Analyze"
5. View results: summary, charts, table
6. Download PDF report

---

## ❓ Troubleshooting

**Port 8000 in use?**
```bash
python manage.py runserver 8001
```

**Port 3000 in use?**
```bash
PORT=3001 npm start
```

**Module not found?**
```bash
pip install -r requirements.txt
npm install
```

---

## 📹 Demo Video Script

1. Show backend running (API endpoints)
2. Open web app
3. Register/Login
4. Upload sample CSV
5. Show summary statistics
6. Show bar chart
7. Show pie chart
8. Show data table
9. Download PDF
10. Open desktop app
11. Repeat steps 3-9 in desktop
12. Show both frontends work with same backend

**Record Duration:** 2-3 minutes
**Tools:** OBS Studio, Loom, or Windows Game Bar

---

## ✅ Pre-Submission Checklist

- [ ] All 3 components run without errors
- [ ] CSV upload works
- [ ] Charts display correctly
- [ ] PDF downloads successfully
- [ ] Authentication works
- [ ] Last 5 datasets are stored
- [ ] Demo video recorded
- [ ] Code pushed to GitHub
- [ ] README is complete
- [ ] Form submitted

Good luck! 🎉
