from flask import Flask, request, jsonify
from hdLessDexScn import multiThread
import threading
app = Flask(__name__)


def background_task(dexUrl, token_pair):
    """Function to run in the background."""
    multiThread(dexUrl=dexUrl, token_pair=token_pair)

# API endpoint to generate a URL based on blockchain and pairAddress
@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    dexType = data.get('dexType')
    blockchain = data.get('blockchain')
    pairAddress = data.get('pairAddress')

    # Check if both parameters are provided
    if not blockchain or not pairAddress:
        return jsonify({'error': "Both 'blockchain' and 'pairAddress' parameters are required."}), 400

    # Construct the URL with the provided parameters
    print(dexType,pairAddress)
    # jsonify({'url': generated_url})
    thread = threading.Thread(target=background_task, args=(dexType, pairAddress))
    thread.start()
    generated_url = f'https://{dexType}/{pairAddress}'
    # Send the generated URL back as a response
    return jsonify({'url': generated_url})

@app.route('/', methods=['Get'])
def print_hello_world():
    print('hello_world')
    return jsonify({'url': 'hello_world'})




# Start the server and listen on the specified port
if __name__ == '__main__':
    app.run(port=3000, debug=True)

