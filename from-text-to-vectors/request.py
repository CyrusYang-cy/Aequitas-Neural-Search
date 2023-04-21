import requests
import json
import sys
from sentence_transformers import SentenceTransformer

# A sentence to encode
# sentence = ["what is the gre test"]
sentence = [sys.argv[1]]  # Get the sentence from the command line argument

# Load or create a SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Compute sentence embeddings
embeddings = model.encode(sentence)

# Create an array of floats comma separated (removing the initial "array" string and the trailing "dtype=float32")
vector_embeddings = repr(list(embeddings)[0])[6:-22]

# Replace with the URL you want to send the request to
url = 'http://localhost:8983/solr/neural/select?fl=id,text,score'
query = {
    "query": "{!knn f=vector topK=3}" + vector_embeddings
}
headers = {
    "Content-type": "application/json"
}

response = requests.post(url, data=json.dumps(query), headers=headers)

# print(response.text)  # This will print the returned result
# Parse the JSON response and print only the 'response' dictionary
response_json = json.loads(response.text)
print(json.dumps(response_json['response'], indent=2))
