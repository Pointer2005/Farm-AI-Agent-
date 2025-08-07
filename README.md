
# 🌱 Farm AI Agent – AI-Powered Crop Recommendation System

An AI-powered web application that helps farmers make data-driven decisions on **crop selection**, **fertilizer use**, **pesticide recommendations**, and **sustainable farming practices**.
It uses **Google's Gemini API** to analyze soil, weather, and location data and generate detailed farming advice aligned with **UN SDG 2 (Zero Hunger)**.

---

## 🚀 Features

* **Soil Data Analysis** – pH, nutrient content, organic matter, and moisture.
* **Weather-Based Recommendations** – temperature, humidity, rainfall, sunlight hours, and season.
* **Location-Based Customization** – region, climate zone, and altitude.
* **AI-Generated Insights** – recommended crops, fertilizers, pesticides, soil improvement tips, and sustainability practices.
* **Interactive Web UI** – responsive, theme-switching (light/dark mode), and accessible.
* **REST API Support** – endpoints for health check and AI analysis.

---

## 📂 Project Structure

```
├── app.py          # Flask backend with Gemini API integration
├── templates/
│   └── index.html  # Frontend user interface
└── README.md       # Project documentation
```

---

## ⚙️ Requirements

### Backend

* Python 3.8+
* Flask
* Flask-CORS
* python-dotenv
* google-generativeai

Install dependencies:

```bash
pip install flask flask-cors python-dotenv google-generativeai
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root and add:

```
API_KEY=your_gemini_api_key_here
```

You can get your **Gemini API key** from the [Google AI Studio](https://aistudio.google.com/).

---

## ▶️ Running the Application

1. **Clone the repository**

   ```bash
   git clone https://github.com/Pointer2005/Farm-AI-Agent-.git
   cd Farm-AI-Agent
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key** in `.env`.

4. **Run the server**

   ```bash
   python app.py
   ```

5. Open your browser and visit:

   ```
   http://127.0.0.1:5000
   ```

---

## 🌐 API Endpoints

### 1. **Health Check**

```
GET /api/health
```

**Response:**

```json
{
  "status": "healthy",
  "gemini_configured": true,
  "timestamp": "2025-08-07T09:30:00"
}
```

### 2. **Analyze Farming Data**

```
POST /api/analyze
```

**Body (JSON):**

```json
{
  "soil_data": {
    "soil_type": "loamy",
    "ph_level": 6.5,
    "nitrogen": 200,
    "phosphorus": 50,
    "potassium": 150,
    "organic_matter": 3.5,
    "moisture": 25
  },
  "weather_data": {
    "avg_temperature": 25.5,
    "humidity": 65,
    "rainfall": 1200,
    "season": "monsoon",
    "sunlight_hours": 8.5
  },
  "location_data": {
    "region": "Maharashtra, India",
    "climate_zone": "tropical",
    "altitude": 500
  }
}
```

**Response:** AI-generated recommendations in JSON.

---

## 🎨 Frontend Features

* Modern **light/dark** theme toggle.
* Fully **responsive** UI for mobile, tablet, and desktop.
* **Loading animations** during AI analysis.
* Well-structured **form sections** for soil, weather, and location data.
* Displays AI results in **cards and sections** with icons.

---

## 📌 Notes

* Make sure your Gemini API key has **Generative AI access**.
* The AI may return raw text if it cannot format the output in JSON.

----

## 📜 License

This project is licensed under the MIT License – feel free to use and modify.

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Pointer2005/Farm-AI-Agent-.git
git push -u origin main
