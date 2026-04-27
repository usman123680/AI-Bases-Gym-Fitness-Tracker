from flask import Flask, render_template, jsonify
import subprocess
from flask_cors import CORS  
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    # Get user's home directory
    home_dir = os.path.expanduser("~")
    script_path = os.path.join(home_dir, 'Desktop', 'Gym_Fitness_Tracker_app', 'main.py') #change to .py
    
    # Start the script
    subprocess.Popen(['python', script_path])
    return jsonify({"message": "Started the process!"})

if __name__ == '__main__':
    app.run(debug=True)