import os
import subprocess
import threading
from flask import Flask, request, jsonify
import logging

# Configure logging to file
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='app.log',  # Log will be written to 'app.log'
                    filemode='w')  # Use 'a' to append to the file instead of 'w' to overwrite

app = Flask(__name__)

# List to keep track of subprocesses
subprocesses = []

def start_subprocess(command):  
    """Starts a subprocess and keeps track of it."""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocesses.append(process)
        logging.info(f"Started subprocess {process.pid} with command: {' '.join(command)}")
        return process
    except Exception as e:
        logging.error(f"Error starting subprocess with command {command}: {e}")
        raise

def kill_all_subprocesses():
    """Terminates all tracked subprocesses."""
    for process in subprocesses:
        try:
            process.terminate()
            process.wait()
            logging.info(f"Process {process.pid} terminated")
        except Exception as e:
            logging.error(f"Failed to terminate process {process.pid}: {e}")

def setup_environment(pair_address):
    """Set up and return the virtual environment directory."""
    env_dir = f"./venvs/{pair_address.replace(':', '_')}"
    os.makedirs(env_dir, exist_ok=True)
    logging.debug(f'Folder for env: {env_dir}')
    return env_dir

def create_and_run_bot(dex_url, blockchain, pair_address): 
    """Sets up environment and runs the bot script in a subprocess."""
    env_dir = setup_environment(pair_address)
    subprocess.run(["python", "-m", "venv", env_dir], check=True)
    
    scripts_dir = "Scripts" if os.name == 'nt' else "bin"
    pip_path = os.path.join(env_dir, scripts_dir, "pip")
    python_path = os.path.join(env_dir, scripts_dir, "python")
    print(pip_path)
    print(python_path)
    # subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)

    # Install dependencies
    subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    subprocess.run([pip_path, "install", "selenium", "flask", "selenium-wire", "blinker==1.7.0", "mitmproxy"], check=True)
    
    # Execute bot script in a subprocess
    bot_script_path = "bot_script.py"
    try:
        subprocess.run([python_path, bot_script_path, dex_url, blockchain, pair_address], check=True)
        logging.info(f"Bot script {bot_script_path} started successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess failed with return code {e.returncode}. Output: {e.output}")
        raise

def background_task(dex_url, blockchain, pair_address):
    """Background task that runs the bot."""
    create_and_run_bot(dex_url, blockchain, pair_address)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    """API endpoint to start the bot and generate a URL."""
    try:
        data = request.get_json()
        dex_url = data.get('dexType')
        blockchain = data.get('blockchain')
        pair_address = data.get('pairAddress')

        if not blockchain or not pair_address:
            return jsonify({'error': "Both 'blockchain' and 'pairAddress' are required."}), 400

        thread = threading.Thread(target=background_task, args=(dex_url, blockchain, pair_address))
        thread.start()
        logging.debug(f"Thread started for {dex_url}{blockchain}{pair_address}")

        generated_url = f'{dex_url}{blockchain}{pair_address}'
        return jsonify({
            'statusCode': '200',
            'status': 'success',
            'Bot progress': 'Your bot is running',
            'url': generated_url
        })
    except Exception as e:
        logging.error(f"Error in generate-url endpoint: {e}")
        return jsonify({'error': str(e)})

@app.route('/kill-subprocesses', methods=['POST'])
def kill_subprocesses():
    """API endpoint to terminate all subprocesses."""
    kill_all_subprocesses()
    return jsonify({'status': 'success', 'message': 'All subprocesses have been terminated'})

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, world!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
