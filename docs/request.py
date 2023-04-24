import requests
import json
import sys
import argparse
import urllib.parse
from sentence_transformers import SentenceTransformer

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--query", help="the query to execute", required=True)
parser.add_argument(
    "--keywords", help="the list of keywords that must include")
parser.add_argument("--boolean", help="the boolean operator to use for keywords (AND/OR)",
                    choices=["OR", "AND"], default="AND")
args = parser.parse_args()
if args.keywords:
    keywords = args.keywords.split(",")
else:
    keywords = "*"

# Load or create a SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Compute sentence embeddings
embeddings = model.encode([args.query])

# Create an array of floats comma separated (removing the initial "array" string and the trailing "dtype=float32")
vector_embeddings = repr(list(embeddings)[0])[6:-22]

# Replace with the URL you want to send the request to
url = 'http://localhost:8983/solr/aequitas_test/select'
# set the query parameters
params = {
    'fl': 'id, title, score, content',
}
query = {
    "query": "{!knn f=vector topK=3}" + vector_embeddings,
    # "filter": "content: {keyword}".format(keyword=keyword),
    "filter": "content:({})".format(" {} ".format(args.boolean).join(keywords)),
}
headers = {
    "Content-type": "application/json"
}

response = requests.post(url, data=json.dumps(
    query), headers=headers, params=params)

# Parse the JSON response and print only the 'response' dictionary
response_json = json.loads(response.text)
print(json.dumps(response_json['response'], indent=2))
