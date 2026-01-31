# 🧪 Chemical Equipment Parameter Visualizer
## Hybrid Web + Desktop Application

**FOSSEE Semester Long Internship 2026 - Screening Task Submission**

A full-stack hybrid application for analyzing and visualizing chemical equipment data. Upload CSV files and get instant analytics, charts, and PDF reports - available both as a web app and desktop application!

---

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Demo Video](#demo-video)

---

## ✨ Features

### Core Features
✅ **CSV Upload** - Upload chemical equipment data via web or desktop  
✅ **Data Analysis** - Automatic calculation of summary statistics  
✅ **Visualizations** - Interactive charts (Bar & Pie charts)  
✅ **History Management** - Stores last 5 uploaded datasets  
✅ **PDF Reports** - Generate downloadable analysis reports  
✅ **Authentication** - User login/register system  
✅ **Hybrid Architecture** - Same backend serves both web and desktop clients  

### Technical Features
- RESTful API with Django REST Framework
- Responsive React.js web interface
- Native PyQt5 desktop application
- SQLite database for data persistence
- Pandas for data processing
- Chart.js (Web) & Matplotlib (Desktop) for visualizations

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python Django + DRF | REST API server |
| **Frontend (Web)** | React.js + Chart.js | Web interface |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Desktop application |
| **Data Processing** | Pandas | CSV analysis |
| **Database** | SQLite | Data storage |
| **PDF Generation** | ReportLab | PDF reports |

---

## 📁 Project Structure

```
hybrid-chemical-visualizer/
├── backend/                          # Django REST API
│   ├── api/
│   │   ├── models.py                # Database models
│   │   ├── views.py                 # API endpoints
│   │   ├── serializers.py           # Data serialization
│   │   └── urls.py                  # API routing
│   ├── chemical_visualizer/
│   │   ├── settings.py              # Django settings
│   │   └── urls.py                  # Main URL config
│   ├── manage.py
│   └── requirements.txt
│
├── frontend-web/                     # React.js Web App
│   ├── src/
│   │   ├── App.js                   # Main React component
│   │   └── App.css                  # Styles
│   ├── package.json
│   └── public/
│
├── frontend-desktop/                 # PyQt5 Desktop App
│   ├── main.py                      # Desktop application
│   └── requirements.txt
│
├── sample_equipment_data.csv         # Sample test data
└── README.md                         # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ and npm
- Git

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd hybrid-chemical-visualizer
```

### Step 2: Backend Setup (Django)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create Django app directory
mkdir api
cd api
touch __init__.py models.py views.py serializers.py urls.py admin.py apps.py
cd ..

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

Backend will run on: `http://localhost:8000`

### Step 3: Web Frontend Setup (React)

Open a new terminal:

```bash
cd frontend-web

# Install dependencies
npm install

# Start React development server
npm start
```

Web app will open at: `http://localhost:3000`

### Step 4: Desktop Frontend Setup (PyQt5)

Open another terminal:

```bash
cd frontend-desktop

# Create virtual environment (separate from backend)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

---

## 📖 Usage Guide

### Web Application

1. **Open Browser** → Navigate to `http://localhost:3000`
2. **Register/Login** (Optional) → Create account or login
3. **Upload CSV**:
   - Click "Choose File"
   - Select `sample_equipment_data.csv`
   - Click "Upload & Analyze"
4. **View Results**:
   - Summary statistics
   - Bar chart (average values)
   - Pie chart (equipment types)
   - Data table
5. **Download PDF** → Click "Download PDF" button

### Desktop Application

1. **Launch App** → Run `python main.py`
2. **Login** (Optional) → Enter credentials
3. **Upload CSV**:
   - Click "Select CSV File"
   - Choose file
   - Click "Upload & Analyze"
4. **View Data**:
   - Switch between tabs: Summary, Data Table, Charts
   - Select datasets from dropdown
5. **Generate PDF** → Click "Download PDF Report"

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register/      - Register new user
POST   /api/auth/login/         - User login
POST   /api/auth/logout/        - User logout
GET    /api/auth/status/        - Check auth status
```

### Datasets
```
GET    /api/datasets/           - List last 5 datasets
POST   /api/datasets/upload/    - Upload CSV file
GET    /api/datasets/{id}/      - Get dataset details
GET    /api/datasets/{id}/generate_pdf/  - Generate PDF report
```

### Example API Call

```bash
# Upload CSV
curl -X POST http://localhost:8000/api/datasets/upload/ \
  -F "file=@sample_equipment_data.csv"

# Get datasets
curl http://localhost:8000/api/datasets/
```

---

## 📊 CSV File Format

Your CSV must have these columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Centrifugal Pump,250.5,15.2,85.3
Heat Exchanger-HX01,Shell and Tube,180.0,12.5,120.5
...
```

**Required Columns:**
- `Equipment Name` - String
- `Type` - String (equipment category)
- `Flowrate` - Float
- `Pressure` - Float
- `Temperature` - Float

---

## 🎥 Demo Video

**Video Link:** [Insert your demo video link here]

**Video Contents:**
- Web app demonstration (upload, visualize, PDF)
- Desktop app demonstration
- API testing
- Features showcase

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Port already in use**
```bash
# Change Django port
python manage.py runserver 8001

# Change React port
PORT=3001 npm start
```

**Issue: CORS errors**
- Ensure Django backend is running
- Check CORS settings in `backend/chemical_visualizer/settings.py`

**Issue: Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt
npm install
```

**Issue: Database locked**
```bash
# Delete and recreate database
rm backend/db.sqlite3
python manage.py migrate
```

---

## 📝 Additional Features Implemented

### Extra Credit Features ⭐
1. ✅ **PDF Report Generation** - Complete analysis reports
2. ✅ **User Authentication** - Login/Register system
3. ✅ **History Management** - Last 5 datasets stored
4. ✅ **Responsive Design** - Works on mobile/tablet
5. ✅ **Error Handling** - Comprehensive error messages
6. ✅ **Data Validation** - CSV format checking

---

## 🧪 Testing

### Test with Sample Data

```bash
# Use provided sample CSV
sample_equipment_data.csv (included in repo)

# Or create your own following the format above
```

### Manual Testing Checklist

- [ ] Upload CSV successfully
- [ ] View summary statistics
- [ ] See bar chart
- [ ] See pie chart
- [ ] View data table
- [ ] Download PDF report
- [ ] Login/Register
- [ ] Switch between datasets
- [ ] Desktop app functionality

---

## 👨‍💻 Development

### Run in Development Mode

```bash
# Backend (with auto-reload)
python manage.py runserver

# Frontend Web (with hot reload)
npm start

# Desktop (restart manually after changes)
python main.py
```

### Database Management

```bash
# Reset database
python manage.py flush

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

---

## 📦 Deployment (Optional)

### Web Deployment Options
- **Heroku** - Backend + Frontend
- **Vercel** - Frontend only
- **Railway** - Full stack
- **PythonAnywhere** - Backend only

### Example: Heroku Deployment
```bash
# Add Procfile
echo "web: gunicorn chemical_visualizer.wsgi" > Procfile

# Deploy
heroku create
git push heroku main
```

---

## 🤝 Contributing

This is a screening task submission. Contributions are not accepted.

---

## 📄 License

This project is created for FOSSEE Semester Long Internship 2026 screening task.

---

## 📧 Contact

**Candidate Name:** [Your Name]  
**Email:** [your.email@example.com]  
**GitHub:** [your-github-username]  

---

## ✅ Submission Checklist

- [x] Backend with Django + DRF
- [x] Web frontend with React.js + Chart.js
- [x] Desktop frontend with PyQt5 + Matplotlib
- [x] CSV upload functionality
- [x] Data summary API
- [x] Visualizations (charts)
- [x] Last 5 datasets storage
- [x] PDF report generation
- [x] Basic authentication
- [x] Sample CSV provided
- [x] README with setup instructions
- [x] Demo video recorded
- [ ] GitHub repository link
- [ ] Submission form filled

---

**Made with ❤️ for FOSSEE Internship 2026**
