from click.testing import CliRunner
import unittest
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from fetch_data import download_data


class DownloadDataTest(unittest.TestCase):

    def setUp(self):
        self.date_from = '2022-12-02'
        self.date_to = '2022-12-03'
        self.date_from_tge = datetime.strftime(
            date.today() - relativedelta(months=2), '%Y-%m-%d')
        self.date_to_tge = datetime.strftime(
            date.today() - relativedelta(months=2) + timedelta(days=1), '%Y-%m-%d')
        self.date_from_tge_far = datetime.strftime(
            date.today() - relativedelta(months=4), '%Y-%m-%d')

    def test_download_data_option_1(self):
        runner = CliRunner()
        result = runner.invoke(download_data, [
                               '--number', '1', '--date_from', self.date_from, '--date_to', self.date_to])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '1', '--date_from', self.date_from, '--date_to', self.date_to, '--folder_path', '', '--statistics', 'y'])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '1', '--date_from', self.date_from, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '1', '--date_from', self.date_to, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '1', '--date_from', 'test_date', '--date_to', 'test_date_2'])
        self.assertEqual(result.exit_code, 1)

    def test_download_data_option_2(self):
        runner = CliRunner()
        result = runner.invoke(download_data, [
                               '--number', '2', '--date_from', self.date_from, '--date_to', self.date_to])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '2', '--date_from', self.date_from, '--date_to', self.date_to, '--folder_path', '', '--statistics', 'y'])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '2', '--date_from', self.date_from, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '2', '--date_from', self.date_to, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '2', '--date_from', 'test_date', '--date_to', 'test_date_2'])
        self.assertEqual(result.exit_code, 1)

    def test_download_data_option_3(self):
        runner = CliRunner()
        result = runner.invoke(download_data, [
                               '--number', '3', '--date_from', self.date_from_tge, '--date_to', self.date_to_tge])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '3', '--date_from', self.date_from_tge, '--date_to', self.date_to_tge, '--folder_path', '', '--statistics', 'y'])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '3', '--date_from', self.date_from_tge, '--date_to', self.date_from_tge])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(download_data, [
                               '--number', '3', '--date_from', self.date_to_tge, '--date_to', self.date_from_tge])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '3', '--date_from', 'test_date', '--date_to', 'test_date_2'])
        self.assertEqual(result.exit_code, 1)

    def test_download_data_option_other(self):
        runner = CliRunner()
        result = runner.invoke(download_data, [
                               '--number', '4', '--date_from', self.date_from, '--date_to', self.date_to])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', 's', '--date_from', self.date_from, '--date_to', self.date_to])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '-1', '--date_from', self.date_from, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '0', '--date_from', self.date_from, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)

        result = runner.invoke(download_data, [
                               '--number', '', '--date_from', self.date_from, '--date_to', self.date_from])
        self.assertEqual(result.exit_code, 1)


if __name__ == '__main__':
    unittest.main()
