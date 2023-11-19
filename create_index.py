import os
import json 
import re
from bs4 import BeautifulSoup

HTML_DIR = './html'

def tokenize(text):
    tokens = re.findall(r'\w+', text)
    return tokens

def get_descriptive_content(file_name):
    DESCRIPTIVE_CONTENT_SELECTOR = '#mw-content-text > div.mw-content-ltr.mw-parser-output > table + p:not(.mw-empty-elt)'
    with open(os.path.join(HTML_DIR, file_name)) as f:
        
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

        return soup.select(DESCRIPTIVE_CONTENT_SELECTOR)[0].get_text()

def update_inverted_index(doc_id, descriptive_content_tokenized, inverted_index):
    
    for position, token in enumerate(descriptive_content_tokenized):
        token = str.lower(token)
        if token not in inverted_index:
            inverted_index[token] = []
 
        if token in inverted_index:
            postings = inverted_index[token]
            posting = f'{doc_id},{position}'
            if posting not in postings:
                inverted_index[token].append(posting)

    return inverted_index

def main():
    documents = {}
    inverted_index = {}
    print("Creating index...")

    for doc_id, file_name in enumerate(os.listdir(HTML_DIR)):

        if file_name.endswith('.html'):

            documents[doc_id] = file_name

            descriptive_content = get_descriptive_content(file_name)
            descriptive_content_tokenized = tokenize(descriptive_content)
            inverted_index = update_inverted_index(doc_id, descriptive_content_tokenized, inverted_index)

    with open(f"./inverted_index.json", "w") as file:
        index = {
            "documents": documents,
            "inverted_index": inverted_index
        }

        json.dump(index, file)

    print("Index created!")

main()