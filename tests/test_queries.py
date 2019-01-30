import unittest
from queries import get_score_name, get_score_number, get_results


class QueriesTestCase(unittest.TestCase):

    def test_get_score_name(self):
        string_1 = "test"
        string_2 = "test"
        self.assertEqual(get_score_name(string_1, string_2), 1.0)

    def test_get_score_number(self):
        actual_number = 100
        query_number = 99
        max_number = 100
        self.assertAlmostEqual(get_score_number(query_number, actual_number, max_number), 0.99)

    def test_get_results(self):
        index = [{"name": 'test1', "population": 100, "lat": 10, "long": -15},
                 {"name": 'other2', "population": 300, "lat": 30, "long": -35},
                 {"name": 'other3', "population": 400, "lat": 40, "long": -45}]
        name = "test1"
        population = 100
        latitude = 10
        longitude = -15
        self.assertEqual(get_results(name, population, latitude, longitude, index), [{"name": 'test1', "population": 100, "lat": 10, "long": -15, "score": 1.0}])


if __name__ == '__main__':
    unittest.main()
