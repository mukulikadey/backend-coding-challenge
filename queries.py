
import json
from difflib import SequenceMatcher
from operator import itemgetter


def get_index():
    """
    This loads our search index.

    :return: a list of cities as dictionary objects.
    """

    with open('search_indexer.json', 'r') as file:
        return json.load(file)


def get_score_name(query_name, actual_name):
    """
    This gets the score for name queries.

    :param query_name: the query name that the user inputs.
    :param actual_name: the city name in our index.
    :return: similarity score between the query and actual name.
    """

    return SequenceMatcher(lambda x: x == ' ', actual_name, query_name).ratio()


def get_score_number(query_num, actual_num, max_num):
    """
    This gets the score for numeric query parameters.

    :param query_num: the numeric query that the user inputs.
    :param actual_num: the city's numeric value in our index - can be lat, long, or pop.
    :param max_num: the maximum value for that numeric property.
    :return: the normalized score between the query and actual name.
    """

    score = (1 - abs(actual_num - query_num) / float(max_num)) if (max_num != 0) else 0

    return score


def get_results(name, population, lat, long, cities):
    """
    This gets the sorted results based on query parameters.

    :param name: the query name that the user inputs.
    :param population: the query population that the user inputs.
    :param lat: the query latitude that the user inputs.
    :param long: the query longitude that the user inputs.
    :param cities: the list of cities in our index.
    :return: the relevant results based on user query in decreasing order of scores.
    """

    results = []

    max_pop = 0
    max_lat = 0.0
    max_long = 0.0

    # calculate the maximum values for each numeric query parameter
    for city in cities:
        if city['population'] > max_pop:
            max_pop = city['population']
        if abs(city['lat']) > max_lat:
            max_lat = abs(city['lat'])
        if abs(city['long']) > max_long:
            max_long = abs(city['long'])

    # calculate score for each query parameter
    for city in cities:
        score_list = []

        if population is not 0:
            score_pop = get_score_number(population, city['population'], max_pop)
            score_list.append(score_pop)
        if abs(long) > 0.000001:
            score_long = get_score_number(long, city['long'], max_long)
            score_list.append(score_long)
        if abs(lat) > 0.000001:
            score_lat = get_score_number(lat, city['lat'], max_lat)
            score_list.append(score_lat)
        if name is not None:
            score_name = get_score_name(name, city['name'])
            score_list.append(score_name)

        total_score = sum(score_list) / len(score_list)

        city['score'] = total_score

        if city['score'] >= 0.5:
            results.append(city)

    sorted_results = sorted(results, key=itemgetter('score'), reverse=True)

    return sorted_results
