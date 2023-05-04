import requests
import re


def clean(input_str):
    input_str = input_str.replace('\n', '').replace('\t', '')
    input_str = re.sub('\.{4,}', '', input_str)
    return input_str


def extract(input_str):
    if len(input_str) < 100:
        return "null"
    words = input_str.split()
    if len(words) > 250:
        return ' '.join(words[:250])
    return input_str


# set the URL of the Solr API endpoint
url = 'http://solr.aequitasdocs.org:8983/solr/aequitas_documents/select'

# set the query parameters
params = {
    'q': '*:*',
    'q.op': 'OR',
    'fl': 'title, content',
    'indent': 'true',
    'rows': '3424',
}

# set the authentication credentials
auth = ('admin', '1o8HithlBo-Riwl8')

# send a GET request to the Solr API endpoint with the query parameters and authentication credentials
response = requests.get(url, params=params, auth=auth)

# extract the titles from the response
# id = [doc['id'][0] for doc in response.json()['response']['docs']]

# write the titles to a TSV file
with open('aequtias_title.tsv', 'w') as f1:
    with open('aequtias_content.tsv', 'w') as f2:
        for doc in response.json()["response"]["docs"]:
            title = clean(doc["title"][0]) if "title" in doc else ""
            content = extract(clean(doc["content"][0])
                              ) if "content" in doc else ""
            f1.write(title + '\t\n')
            f2.write(content + '\t\n')
