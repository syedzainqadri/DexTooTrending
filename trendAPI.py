from flask import Flask, request, jsonify
from hdLessDexScn import run_bot

app = Flask(__name__)

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
    run_bot(dexUrl=dexType,token_pair=pairAddress)
    generated_url = f'https://{dexType}/{pairAddress}'

    # Send the generated URL back as a response
    return jsonify({'url': generated_url})

# Start the server and listen on the specified port
if __name__ == '__main__':
    app.run(port=3000, debug=True)
