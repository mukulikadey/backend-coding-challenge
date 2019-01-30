
import os
import pandas as pd
import json


# convert the tsv file to a json file
def convert_to_json(file):
    file.to_json('data.json', date_format='iso', orient='records')


# create a new list of dictionaries with the keys of interest: name, lat, long, population
def create_docs_of_interest():
    output_json_list = json.load(open('data.json'))
    tuple_keys = ('name', 'lat', 'long', 'population')

    # for every key in the tuple, check if the key exists in the new_dict_list
    # if the key does not exist, then add it to the new_dict_list with it's corresponding value
    new_dict_list = [dict((k, d[k]) for k in tuple_keys if k in d) for d in output_json_list]

    # delete this json file with the data since its content has been migrated
    os.remove("data.json")

    return new_dict_list


# dump our indexer to a json file
def create_indexer(docs):
    with open('search_indexer.json', 'w') as outfile:
        json.dump(docs, outfile)


if __name__ == "__main__":
    tsv_file = pd.read_csv('data/cities_canada-usa.tsv', sep='\t', encoding='utf-8')
    convert_to_json(tsv_file)
    documents = create_docs_of_interest()
    create_indexer(documents)
