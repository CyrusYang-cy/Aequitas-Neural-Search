import pysolr
import sys

# Set up a Solr instance
SOLR_ADDRESS = 'http://localhost:8983/solr/aequitas_test'
solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)

# Define the ID of the document to update
doc_id = sys.argv[1]

# Define the new value for the content field
new_title = sys.argv[2]

# Get the existing document from Solr
results = solr.search(f'id:{doc_id}')
existing_doc = results.docs[0]

# Update the content field in the existing document
print(existing_doc['title'])
existing_doc['title'] = new_title

# Add the updated document to Solr, overwriting the existing document
solr.add([existing_doc], overwrite=True)
