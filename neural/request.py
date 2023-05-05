import requests
import json
import sys
import argparse
import urllib.parse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--query", help="the query to execute", required=True)
parser.add_argument(
    "--keywords", help="the list of keywords that must include")
parser.add_argument("--connectives", help="the connectives operator to use for keywords (AND/OR)",
                    choices=["OR", "AND"], default="AND")
args = parser.parse_args()
if args.keywords:
    keywords = args.keywords.split(",")
else:
    keywords = "*"

# url = 'http://localhost:5001/solr/search'
url = 'http://107.22.6.9:5001/solr/search'
# set the query parameters
params = {
    'fl': 'id, title, score, content',
    'q': args.query,
    'keywords': keywords,
    'connectives': args.connectives
}
headers = {
    "Content-type": "application/json"
}

response = requests.get(url, headers=headers, params=params)

# Parse the JSON response and print only the 'response' dictionary
response_json = json.loads(response.text)
print(json.dumps(response_json['docs'], indent=2))
