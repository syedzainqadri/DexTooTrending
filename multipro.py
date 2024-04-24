import os
import subprocess
import threading
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

def create_and_run_bot(dexUrl, pairAddress):
    # Unique environment directory
    # try:
    # env_dir = f"env_{datetime.now().strftime('%Y%m%D%H%M%S')}+{pairAddress.replace(':', '_')}"  # Sanitize pairAddress to be used in file paths
    # os.makedirs(env_dir, exist_ok=True)
    # except:
    env_dir = f"./venvs/{pairAddress.replace(':', '_')}"  # Sanitize pairAddress to be used in file paths
    os.makedirs(env_dir, exist_ok=True)

    # Create a virtual environment
    subprocess.run(["python", "-m", "venv", env_dir])
    
    # Activate the environment and install dependencies
    # Adjust the path to pip and python depending on the OS
    pip_path = os.path.join(env_dir, "Scripts", "pip")
    python_path = os.path.join(env_dir, "Scripts", "python")

    # Install required packages
    print("Python Path:", python_path)
    print("Pip Path:", pip_path)
    subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    subprocess.run([pip_path, "install", "selenium", "flask", "selenium-wire"], check=True)

    # Execute the bot script
    # Assume bot's actions are defined in a function `run_bot` inside bot_script.py
    bot_script_path = "bot_script.py"  # Path to your bot script
    subprocess.run([python_path, bot_script_path, dexUrl, pairAddress])

def background_task(dexUrl, pairAddress):
    """Function to run in the background."""
    create_and_run_bot(dexUrl, pairAddress)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    dexType = data.get('dexType')
    blockchain = data.get('blockchain')
    pairAddress = data.get('pairAddress')

    if not blockchain or not pairAddress:
        return jsonify({'error': "Both 'blockchain' and 'pairAddress' parameters are required."}), 400

    thread = threading.Thread(target=background_task, args=(dexType, pairAddress))
    thread.start()
    
    generated_url = f'{dexType}{pairAddress}'
    return jsonify({
        'statusCode': '200',
        'status': 'success',
        'Bot progress': 'Your bot is running',
        'url': generated_url
    })

@app.route('/', methods=['GET'])
def print_hello_world():
    return jsonify({'message': 'hello_world'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
