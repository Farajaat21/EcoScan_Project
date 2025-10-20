# 🌳 EcoScan - Sustainable Shopping Made Simple

**Welcome to EcoScan, your smarter way to shop sustainably. Instantly scan products to discover their environmental impact and make eco-friendly choices with confidence.**

## 🚀 Features

- **📱 Instant Barcode Scanning**: Point your camera at any product barcode to get instant environmental impact analysis
- **🌱 Sustainability Scoring**: Get detailed breakdowns of carbon footprint, water usage, and other environmental factors
- **💡 Smart Recommendations**: Receive personalized suggestions for more sustainable alternatives
- **📊 Visual Impact Breakdown**: Easy-to-understand charts and progress bars showing environmental impact
- **📱 Mobile-Friendly**: Responsive design that works perfectly on mobile devices

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Dependencies and Requirements
- **Python 3.13+**: Core backend language
- **SQLAlchemy**: Database ORM
- **Uvicorn**: ASGI server

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Responsive design with modern styling
- **JavaScript**: Interactive functionality and barcode scanning
- **QuaggaJS**: Barcode detection library

## 📋 Prerequisites

- Python 3.13 or higher
- Modern web browser with camera access
- Internet connection for barcode scanning

## 🚀 Quick Start

### Option 1: Using the Startup Script (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd EcoScan_Project
   ```

2. Run the startup script:
   ```bash
   ./start_ecoscan.sh
   ```

3. Open your browser and navigate to:
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Option 2: Manual Setup

1. **Set up the backend**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r backend/requirements.txt
   
   # Start backend server
   python test_server.py
   ```

2. **Set up the frontend** (in a new terminal):
   ```bash
   cd frontend
   python3 -m http.server 3000
   ```

3. **Open your browser** and navigate to http://localhost:3000

## 📱 How to Use

1. **Home Page**: Learn about EcoScan's features and capabilities
2. **Scan Page**: 
   - Click "Start Camera" to begin scanning
   - Point your camera at a product barcode
   - Alternatively, use "Manual Input" to enter a barcode number
3. **Results**: View the sustainability score and environmental impact breakdown
4. **Recommendations**: Get suggestions for more sustainable alternatives

## 🔧 API Endpoints

### GET /api/scan
Scan a product barcode and get environmental impact data.

**Parameters:**
- `barcode` (string): The product barcode to analyze

**Response:**
```json
{
  "barcode": "123456789",
  "score": 75,
  "breakdown": {
    "carbon": 15,
    "water": 8,
    "other": 2
  }
}
```

### GET /
Health check endpoint.

**Response:**
```json
{
  "message": "EcoScan API is running!"
}
```

## 🏗️ Project Structure

```
EcoScan_Project/
├── backend/
│   ├── database.py          # Database configuration
│   ├── eco_data.py          # Environmental impact calculation logic
│   ├── models.py            # Database models
│   ├── server.py            # Main FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Landing page
│   ├── scan.html            # Barcode scanning page
│   ├── styles/
│   │   ├── main.css         # Main stylesheet
│   │   └── resposive.css    # Responsive design styles
│   ├── script/
│   │   └── app.js           # JavaScript functionality
│   └── package.json         # Frontend dependencies
├── start_ecoscan.sh         # Startup script
├── test_server.py           # Simplified test server
└── README.md               # This file
```

## 🌍 Environmental Impact Calculation

EcoScan now supports **real product search** with multiple data sources:

### Real Product Search Capabilities:
- **OpenFoodFacts API**: Real food product database with 1M+ products
- **Web Scraping**: Google Shopping integration for general products
- **Sustainability Scoring**: AI-powered environmental impact calculation
- **Real-time Data**: Live product information and ratings

### Data Sources:
1. **OpenFoodFacts** - Comprehensive food product database
2. **Web Scraping** - Google Shopping for general products
3. **Mock Database** - Fallback for demonstration purposes

### Sustainability Score Algorithm:
- **Food Products**: Based on organic certification, packaging, fair trade, local production
- **General Products**: Keyword analysis for eco-friendly attributes
- **Real-time Calculation**: Dynamic scoring based on available product data

### Future Enhancements:
- Amazon Product API integration
- Google Shopping API
- Carbon footprint calculation APIs
- Machine learning models for accurate sustainability scoring

## 🔮 Future Enhancements

- **Real Product Database**: Integration with actual product databases
- **User Accounts**: Save scan history and preferences
- **Social Features**: Share sustainable choices with friends
- **Store Integration**: Find sustainable alternatives in nearby stores
- **Advanced Analytics**: Track your personal environmental impact over time
- **Mobile App**: Native iOS and Android applications

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- QuaggaJS for barcode detection capabilities
- FastAPI for the excellent web framework
- The sustainability community for inspiration

---

**Make every purchase count for the planet with EcoScan! 🌱**
