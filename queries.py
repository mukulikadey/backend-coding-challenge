import json
from difflib import SequenceMatcher
from operator import itemgetter


# load our search index
def get_index():
    with open('search_indexer.json', 'r') as file:
        return json.load(file)


# gets the score for names
def get_score_name(query_name, actual_name):
    return SequenceMatcher(lambda x: x == " ", actual_name, query_name).ratio()


# gets the score for numeric query parameters
def get_score_number(query_num, actual_num, max_num):
    score = (1 - abs(actual_num - query_num) / max_num) if (max_num != 0) else 0

    return score


# gets sorted results based on query parameters
def get_results(name, population, lat, long):
    results = []
    cities = get_index()

    max_pop = 0
    max_lat = 0.0
    max_long = 0.0

    # calculate the maximum values for each numeric query parameter
    for item in cities:
        if item['population'] > max_pop:
            max_pop = item['population']
        if abs(item['lat']) > max_lat:
            max_lat = abs(item['lat'])
        if abs(item['long']) > max_long:
            max_long = abs(item['long'])

    # calculate score for each query parameter
    for item in cities:
        score_list = []

        if population is not 0:
            score_pop = get_score_number(population, item['population'], max_pop)
            score_list.append(score_pop)
        if abs(long) > 0.000001:
            score_long = get_score_number(long, item['long'], max_long)
            score_list.append(score_long)
        if abs(lat) > 0.000001:
            score_lat = get_score_number(lat, item['lat'], max_lat)
            score_list.append(score_lat)
        if name is not None:
            score_name = get_score_name(name, item['name'])
            score_list.append(score_name)

        total_score = sum(score_list) / len(score_list)

        item['score'] = total_score

        if item['score'] >= 0.5:
            results.append(item)

    sorted_results = sorted(results, key=itemgetter('score'), reverse=True)

    return sorted_results
