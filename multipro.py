import os
import subprocess
import threading
from flask import Flask, request, jsonify
from datetime import datetime
import shutil
app = Flask(__name__)

def sanitize_address(pair_address):
    """Sanitize the pair address to be file system safe."""
    address = str(pair_address.replace(':', '_'))
    return  address

def setup_environment(pair_address):
    """Set up and return the virtual environment directory."""
    env_dir = f"./venvs/{pair_address.replace(':', '_')}"
    os.makedirs(env_dir, exist_ok=True)
    return env_dir

def cleanup_environment(env_dir):
    """Clean up and remove the virtual environment directory."""
    shutil.rmtree(env_dir, ignore_errors=True)

def create_and_run_bot(dex_url, pair_address): 
    env_dir = setup_environment(pair_address)
    subprocess.run(["python", "-m", "venv", env_dir], check=True)
    
    scripts_dir = "Scripts" if os.name == 'nt' else "bin"
    pip_path = os.path.join(env_dir, scripts_dir, "pip")
    python_path = os.path.join(env_dir, scripts_dir, "python")

    # Install dependencies
    print(f"Python Path: {python_path}")
    print(f"Pip Path: {pip_path}")
    subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    subprocess.run([pip_path, "install", "selenium", "flask", "selenium-wire"], check=True)
    
    # Execute bot script
    bot_script_path = "bot_script.py"
    subprocess.run([python_path, bot_script_path, dex_url, pair_address], check=True)
    cleanup_environment(env_dir=env_dir)

def background_task(dex_url, pair_address):
    create_and_run_bot(dex_url, pair_address)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    try:
        data = request.get_json()
        dex_type = data.get('dexType')
        blockchain = data.get('blockchain')
        pair_address = data.get('pairAddress')

        if not blockchain or not pair_address:
            return jsonify({'error': "Both 'blockchain' and 'pairAddress' are required."}), 400

        thread = threading.Thread(target=background_task, args=(dex_type, pair_address))
        thread.start()
        
        generated_url = f'{dex_type}{pair_address}'
        return jsonify({
            'statusCode': '200',
            'status': 'success',
            'Bot progress': 'Your bot is running',
            'url': generated_url
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'hello_world'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
