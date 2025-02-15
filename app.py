import os
import json
import logging
from flask import Flask, jsonify
from scholarship_recommender import ScholarshipRecommender
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Initialize the ScholarshipRecommender
firebase_credentials = json.loads(os.getenv('FIREBASE_CREDENTIALS', '{}'))
scholarship_data_path = os.getenv('SCHOLARSHIP_DATA_PATH', 'data/scholarships.csv')
recommender = ScholarshipRecommender(firebase_credentials, scholarship_data_path)

def update_recommendations():
    recommender.process_users()

# Set up scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_recommendations, trigger="interval", hours=24)
scheduler.start()

@app.route('/')
def home():
    return "Scholarship Recommender is running!"

@app.route('/update', methods=['POST'])
def manual_update():
    recommender.process_users()
    return jsonify({"status": "success", "message": "Recommendations updated"}), 200

@app.route('/test/<user_id>')
def test_user(user_id):
    recommender.test_single_user(user_id)
    return jsonify({"status": "success", "message": f"Tested recommendations for user {user_id}"}), 200

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
