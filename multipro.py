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

import shutil  # Import shutil for removing directory trees

def create_and_run_bot(dex_url, blockchain, pair_address): 
    """Sets up environment, runs the bot script in a subprocess, and cleans up."""
    env_dir = setup_environment(pair_address)
    subprocess.run(["python", "-m", "venv", env_dir], check=True)
    
    scripts_dir = "Scripts" if os.name == 'nt' else "bin"
    python_os = "python" if os.name == 'nt' else "python3"
    pip_path = os.path.join(env_dir, scripts_dir, "pip")
    python_path = os.path.join(env_dir, scripts_dir, python_os)

    # Install dependencies
    subprocess.run([pip_path, "install", "--upgrade", "pip", "setuptools", "wheel"], check=True)
    subprocess.run([pip_path, "install", "selenium", "flask", "selenium-wire", "blinker==1.7.0", "mitmproxy"], check=True)
    
    # Execute bot script in a subprocess
    bot_script_path = "bot_script.py"
    process = None
    try:
        process = subprocess.Popen([python_path, bot_script_path, dex_url, blockchain, pair_address])
        process.wait()  # Wait for the subprocess to finish
        logging.info(f"Bot script {bot_script_path} started and completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess failed with return code {e.returncode}. Output: {e.output}")
        raise
    finally:
        if process is not None:
            # Cleanup: remove virtual environment directory after use
            try:
                shutil.rmtree(env_dir)  # This removes the directory and all its contents
                logging.info(f"Cleaned up virtual environment at {env_dir}")
            except Exception as e:
                logging.error(f"Failed to remove virtual environment at {env_dir}: {e}")

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
