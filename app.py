from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from flask_cors import CORS
import google.generativeai as genai
import os
import json

from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
# Make sure to set your API key in environment variables
GEMINI_API_KEY = os.getenv('API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    model = None

class CropRecommendationAgent:
    def __init__(self):
        self.model = model
    
    def analyze_farming_data(self, soil_data, weather_data, location_data):
        """
        Analyze soil and weather data to recommend crops, fertilizers, and pesticides
        """
        if not self.model:
            return {
                "error": "Gemini API not configured. Please set GEMINI_API_KEY environment variable."
            }
        
        # Construct comprehensive prompt
        prompt = f"""
        As an expert agricultural advisor, analyze the following farming data and provide comprehensive recommendations:

        SOIL DATA:
        - Soil Type: {soil_data.get('soil_type', 'Not specified')}
        - pH Level: {soil_data.get('ph_level', 'Not specified')}
        - Nitrogen (N) Content: {soil_data.get('nitrogen', 'Not specified')} ppm
        - Phosphorus (P) Content: {soil_data.get('phosphorus', 'Not specified')} ppm
        - Potassium (K) Content: {soil_data.get('potassium', 'Not specified')} ppm
        - Organic Matter: {soil_data.get('organic_matter', 'Not specified')}%
        - Moisture Content: {soil_data.get('moisture', 'Not specified')}%

        WEATHER DATA:
        - Average Temperature: {weather_data.get('avg_temperature', 'Not specified')}°C
        - Humidity: {weather_data.get('humidity', 'Not specified')}%
        - Annual Rainfall: {weather_data.get('rainfall', 'Not specified')} mm
        - Season: {weather_data.get('season', 'Not specified')}
        - Sunlight Hours: {weather_data.get('sunlight_hours', 'Not specified')} hours/day

        LOCATION DATA:
        - Region: {location_data.get('region', 'Not specified')}
        - Climate Zone: {location_data.get('climate_zone', 'Not specified')}
        - Altitude: {location_data.get('altitude', 'Not specified')} meters

        Please provide detailed recommendations in the following JSON format:
        {{
            "recommended_crops": [
                {{
                    "crop_name": "Crop Name",
                    "suitability_score": "1-10",
                    "expected_yield": "Expected yield per hectare",
                    "growing_season": "Best time to plant",
                    "reasons": ["Reason 1", "Reason 2"]
                }}
            ],
            "fertilizer_recommendations": [
                {{
                    "fertilizer_type": "Type of fertilizer",
                    "application_rate": "Amount per hectare",
                    "timing": "When to apply",
                    "purpose": "What it addresses"
                }}
            ],
            "pesticide_recommendations": [
                {{
                    "pesticide_type": "Type/Category",
                    "target_pests": ["Pest 1", "Pest 2"],
                    "application_method": "How to apply",
                    "safety_notes": "Safety considerations"
                }}
            ],
            "soil_improvement_suggestions": [
                "Suggestion 1",
                "Suggestion 2"
            ],
            "general_advice": "Overall farming advice for this area",
            "sustainability_tips": [
                "Sustainable practice 1",
                "Sustainable practice 2"
            ]
        }}

        Focus on sustainable farming practices and consider the UN SDG 2 (Zero Hunger) goals. Provide practical, actionable advice.
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                recommendations = json.loads(json_str)
            else:
                # If no JSON found, return raw response
                recommendations = {
                    "raw_response": response_text,
                    "note": "AI response was not in expected JSON format"
                }
            
            return {
                "success": True,
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating recommendations: {str(e)}"
            }

# Initialize the agent
agent = CropRecommendationAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_farming_data():
    try:
        data = request.get_json()
        
        # Validate required data
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        soil_data = data.get('soil_data', {})
        weather_data = data.get('weather_data', {})
        location_data = data.get('location_data', {})
        
        # Get recommendations from AI agent
        result = agent.analyze_farming_data(soil_data, weather_data, location_data)
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "gemini_configured": GEMINI_API_KEY is not None,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Farm AI Agent...")
    print(f"Gemini API configured: {GEMINI_API_KEY is not None}")
    app.run(debug=True, host='0.0.0.0', port=5000)
