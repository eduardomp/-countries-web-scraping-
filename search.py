import sys
import json
from Levenshtein import distance as lev

def load_indexes():
    f = open('inverted_index.json')
    data = json.load(f)

    documents = data['documents']
    inverted_index = data['inverted_index']

    return documents, inverted_index

def country_search(keyword):
    result = "Not found!"

    documents, inverted_index = load_indexes()

    postings = inverted_index.get(keyword, None)
    if postings is not None:
        for posting in postings:
            result = documents[posting.split(',')[0]]
    
    return result

def get_levenshtein_distance(string_1, string_2):
    return lev(string_1, string_2)

def get_similar_keywords_index(keyword, documents, inverted_index):
    similar_keywords_index = {}
    for token in inverted_index:
        distance = get_levenshtein_distance(keyword, token)
        if distance > 0 and distance < 3:
            similar_keywords_index[token] = f' Similar word: {token} - Distance: {distance} - Document: {documents[inverted_index[token][0].split(",")[0]]}'

    return similar_keywords_index

def fuzzy_search(keyword):
    result = ["\t >>>> Not found!"]
    documents, inverted_index = load_indexes()
    # iterate all index getting the distances
    similar_keywords_index = get_similar_keywords_index(keyword, documents, inverted_index)
    
    if len(similar_keywords_index) > 0:
        result = []

    for similar in similar_keywords_index:
        result.append(f'\t >>>> {similar_keywords_index[similar]} \n')

    return result

def main():
    keyword = str.lower(sys.argv[1])

    print('Searching using country_search ...\n')
    print(f'\t >>>> {country_search(keyword)}\n')

    print('Searching using fuzzy_search ...\n')
    for result in fuzzy_search(keyword):
        print(result)


main()