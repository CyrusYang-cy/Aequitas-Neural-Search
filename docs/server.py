from flask import Flask, jsonify, request
import requests
import json
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
# Load or create a SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Compute sentence embeddings

# Define a route for the endpoint
@app.route('/solr/select', methods=['GET'])
def neural_search():
    # Get query parameters from the request
    query = request.args.get('q')
    connectives = request.args.get('connectives', default = 'AND')
    keywords = request.args.get('keywords', default='*')
    keywords = keywords.split(",")
    # Compute sentence embeddings
    embeddings = model.encode([query])
    # Create an array of floats comma separated (removing the initial "array" string and the trailing "dtype=float32")
    vector_embeddings = repr(list(embeddings)[0])[6:-22]

    url = 'http://solr.aequitasdocs.org:8983/solr/aequitas_test/select'
    # set the query parameters
    params = {
        'fl': 'id, title, score',
    }
    query = {
        "query": "{!knn f=vector topK=3}" + vector_embeddings,
        "filter": "content:({})".format(" {} ".format(connectives).join(keywords)),
    }
    headers = {
        "Content-type": "application/json"
    }

    response = requests.post(url, data=json.dumps(
        query), headers=headers, params=params)

    # Parse the JSON response and print only the 'response' dictionary
    response_json = json.loads(response.text)
        
    # Return the response as a JSON object
    return json.dumps(response_json['response'], indent=2)

# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
