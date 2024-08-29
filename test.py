import unittest
from main import merge_lists, sum_values, sum_values_by_month, aggregate_monthly_values

class TestMergeLists(unittest.TestCase):
    def test_equal_length_lists(self):
        result = merge_lists([1, 2, 3], ['a', 'b', 'c'])
        expected = [[1, 'a'], [2, 'b'], [3, 'c']]
        self.assertEqual(result, expected)

    def test_different_length_lists(self):
        result = merge_lists([1, 2], ['a', 'b', 'c'])
        expected = [[1, 'a'], [2, 'b']]
        self.assertEqual(result, expected)

    def test_no_lists(self):
        result = merge_lists()
        expected = []
        self.assertEqual(result, expected)

    def test_empty_lists(self):
        result = merge_lists([], [])
        expected = []
        self.assertEqual(result, expected)

    def test_mixed_length_lists(self):
        result = merge_lists([1, 2, 3], ['a'], [True, False])
        expected = [[1, 'a', True]]
        self.assertEqual(result, expected)

class TestSumValues(unittest.TestCase):
    def test_sum_values_valid(self):
        data = [
            ['2023-01-01', 10],
            ['2023-01-01', 20],
            ['2023-01-02', 30]
        ]
        expected = [
            ['2023-01-01', 30],
            ['2023-01-02', 30]
        ]
        self.assertEqual(sum_values(data), expected)

    def test_sum_values_with_none(self):
        data = [
            ['2023-01-01', 10],
            ['2023-01-01', None],
            ['2023-01-02', 30]
        ]
        expected = [
            ['2023-01-01', 10],
            ['2023-01-02', 30]
        ]
        self.assertEqual(sum_values(data), expected)

    def test_sum_values_empty(self):
        data = []
        expected = []
        self.assertEqual(sum_values(data), expected)

class TestSumValuesByMonth(unittest.TestCase):

    def test_empty_list(self):
        data_value_list = []
        expected_result = []
        self.assertEqual(sum_values_by_month(data_value_list), expected_result)

    def test_list_with_none_values(self):
        data_value_list = [['01012023', None], ['02012023', 10.0], ['01022023', None]]
        expected_result = [['01', 10.0]]
        self.assertEqual(sum_values_by_month(data_value_list), expected_result)

    def test_list_with_valid_values(self):
        data_value_list = [['01012023', 10.0], ['02012023', 20.0], ['01022023', 30.0]]
        expected_result = [['01', 30.0], ['02', 30.0]]
        self.assertEqual(sum_values_by_month(data_value_list), expected_result)

    def test_list_with_rounding(self):
        data_value_list = [['01012023', 10.123], ['02012023', 20.456], ['01022023', 30.789]]
        expected_result = [['01', 30.58], ['02', 30.79]]
        self.assertEqual(sum_values_by_month(data_value_list), expected_result)

class TestAggregateMonthlyValues(unittest.TestCase):
    def test_aggregate_monthly_values(self):
        dados = [
            [(1, 100), (2, 200), (3, 300)],
            [(1, 150), (2, 250), (3, 350)],
            [(1, 200), (2, 300), (3, 400)]
        ]
        resultado_esperado = {
            1: 450,
            2: 750,
            3: 1050
        }
        self.assertEqual(aggregate_monthly_values(dados), resultado_esperado)

    def test_aggregate_with_none_values(self):
        dados = [
            [(1, 100), None, (3, 300)],
            [None, (2, 250), (3, 350)],
            [(1, 200), (2, 300), None]
        ]
        resultado_esperado = {
            1: 300,
            2: 550,
            3: 650
        }
        self.assertEqual(aggregate_monthly_values(dados), resultado_esperado)


if __name__ == '__main__':
    unittest.main()