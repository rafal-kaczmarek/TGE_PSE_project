import unittest
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import fetch_data


class FetchDataTest(unittest.TestCase):

    def setUp(self):
        self.date_from = '2022-12-02'
        self.date_to = '2022-12-10'
        self.url_ok = 'https://httpstat.us/200'
        self.url_fail = 'https://httpstat.us/400'

    def test_get_url_base_link(self):
        self.assertEqual(fetch_data.get_url_base_link(
            1), 'https://www.pse.pl/getcsv/-/export/csv/PL_WYK_KSE/data_od/{}/data_do/{}')
        self.assertEqual(
            fetch_data.get_url_base_link(2), 'https://www.pse.pl/getcsv/-/export/csv/PL_GEN_MOC_JW_EPS/data_od/{}/data_do/{}')
        self.assertEqual(
            fetch_data.get_url_base_link(3), 'https://tge.pl/energia-elektryczna-rdn?dateShow={}')

        with self.assertRaises(Exception):
            fetch_data.get_url_base_link(-1)

        with self.assertRaises(Exception):
            fetch_data.get_url_base_link('s')

    def test_check_connection(self):
        with self.assertRaises(Exception):
            fetch_data.check_connection(self.url_fail)

        assert fetch_data.check_connection(self.url_ok) is None

    def test_check_dates(self):
        self.assertTrue(fetch_data.check_dates(self.date_from, self.date_to))
        self.assertFalse(fetch_data.check_dates(self.date_to, self.date_from))
        self.assertFalse(fetch_data.check_dates(
            self.date_from, self.date_from))

    def test_create_data_periods(self):
        periods = ['02-12-2022', '03-12-2022', '04-12-2022']
        created_periods = fetch_data.create_data_periods(
            '2022-12-02', '2022-12-04')
        self.assertListEqual(periods, created_periods)

        periods = ['2022-12-02 00:00:00',
                   '2022-12-08 12:00:00', '2022-12-15 00:00:00']
        created_periods = [str(x) for x in fetch_data.create_data_periods(
            '2022-12-02', '2022-12-15', 10)]
        self.assertListEqual(periods, created_periods)

        self.assertRaises(Exception, fetch_data.create_data_periods,
                          '2022-12-02', '2022-12-15', -10)

    def test_get_pse_data(self):
        pass

    def test_get_find_variables(self):
        find_variables = fetch_data.get_find_variables(
            'find_test', 'find_id_test')
        self.assertListEqual(find_variables, ['find_test', 'find_id_test'])

    def test_check_tge_date_conditions(self):
        date_from_tge = datetime.strftime(
            date.today() - relativedelta(months=2), '%Y-%m-%d')
        date_to_tge = datetime.strftime(
            date.today() - relativedelta(months=1), '%Y-%m-%d')
        date_from_tge_far = datetime.strftime(
            date.today() - relativedelta(months=4), '%Y-%m-%d')

        self.assertTrue(fetch_data.check_tge_date_conditions(
            date_from_tge, date_to_tge))
        self.assertFalse(fetch_data.check_tge_date_conditions(
            date_to_tge, date_from_tge))
        self.assertTrue(fetch_data.check_tge_date_conditions(
            date_from_tge, date_to_tge))
        self.assertFalse(fetch_data.check_tge_date_conditions(
            date_from_tge_far, date_to_tge))

    def test_get_data_tge(self):
        pass

    def test_get_header(self):
        pass

    def test_create_one_header(self):
        header = fetch_data.create_one_header(['A', 'B'], ['c', 'd', 'd'])
        self.assertListEqual(header, ['Data', 'd', 'A - d', 'B - d'])

    def test_create_own_header(self):
        header = fetch_data.create_own_header('h', 'e', 'ad', 'er')
        self.assertListEqual(header, ['h', 'e', 'ad', 'er'])

    def test_fill_tge_dataframe(self):
        pass

    def test_save_to_csv(self):
        pass


if __name__ == "__main__":
    unittest.main()
