import sys
import pysolr
import time

# Solr configuration
# SOLR_ADDRESS = 'http://localhost:8983/solr/neural'
SOLR_ADDRESS = 'http://localhost:8983/solr/aequitas_test'

BATCH_SIZE = 100
# Create a client instance
solr = pysolr.Solr(SOLR_ADDRESS, always_commit=True)


def index_documents(title, content, embedding):
    # open the file containing text
    with open(title, "r") as title_file:
        # open the file containing vectors
        with open(content, "r") as content_file:
            with open(embedding, "r") as embedding_file:
                documents = []
                # for each document (text and related vector) creates a JSON document
                for index, (title, document, vector_string) in enumerate(zip(title_file, content_file, embedding_file)):

                    vector = [float(w) for w in vector_string.split(",")]
                    doc = {
                        "id": str(index),
                        "title": title,
                        "content": document,
                        "vector": vector
                    }
                    # append JSON document to a list
                    documents.append(doc)

                    # to index batches of documents at a time
                    if index % BATCH_SIZE == 0 and index != 0:
                        # how you'd index data to Solr
                        solr.add(documents)
                        documents = []
                        print("==== indexed {} documents ======".format(index))
                # to index the rest, when 'documents' list < BATCH_SIZE
                if documents:
                    solr.add(documents)
                print("Finished")


def main():
    document_title = sys.argv[1]
    document_content = sys.argv[2]
    embedding_cotent = sys.argv[3]
    initial_time = time.time()
    index_documents(document_title, document_content, embedding_cotent)
    finish_time = time.time()
    print('Documents indexed in {:f} seconds\n'.format(
        finish_time - initial_time))


if __name__ == "__main__":
    main()
