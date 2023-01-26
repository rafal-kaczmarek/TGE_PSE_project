import os
import click
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
import collections
import requests


def get_url_base_link(number):
    '''
    Select source of data from 1 to 3, where: 
    1 - Praca KSE - Wielkości podstawowe 
    2 - Praca KSE - Generacja mocy Jednostek Wytwórczych
    3 - TGE RDN - Kontrakty godzinowe 
    Returns url.
    '''
    if number == 1:
        url_base = 'https://www.pse.pl/getcsv/-/export/csv/PL_WYK_KSE/data_od/{}/data_do/{}'
    elif number == 2:
        url_base = 'https://www.pse.pl/getcsv/-/export/csv/PL_GEN_MOC_JW_EPS/data_od/{}/data_do/{}'
    elif number == 3:
        url_base = 'https://tge.pl/energia-elektryczna-rdn?dateShow={}'
    else:
        raise Exception("Wrong selection. Choose one option from the list.")
    return url_base


def check_connection(url, timeout=5):
    '''
    Checks the connection with the url. If something is wrong, raise error.
    '''
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise errh
    except requests.exceptions.ConnectionError as errc:
        raise errc
    except requests.exceptions.Timeout as errt:
        raise errt
    except requests.exceptions.RequestException as err:
        raise err


def check_dates(date_from, date_to):
    '''
    Check if date_from is below date_to. Dates should be in format YYYY-MM-DD. 
    Returns boolean.
    '''
    return datetime.strptime(date_from, '%Y-%m-%d') < datetime.strptime(date_to, '%Y-%m-%d')


def create_data_periods(date_from, date_to, max_period_days=1):
    '''
    Create list with dates between date_from and date_to and returns list.
    Dates should be in format YYYY-MM-DD.
    If max_period_days is higher than 1 then periods of dates are created. 
    To definie number of periods, number of days between date_from and date_to is divided by max_period_days, rounded up and added 1 to it.
    First period is between list[0] and list[1], second period is between list[1] + 1 day and list[2]. 
    '''
    if max_period_days == 1:
        periods_list = pd.date_range(
            start=date_from, end=date_to, freq='d').strftime('%d-%m-%Y').tolist()
    elif max_period_days > 1:
        periods_num = math.ceil((datetime.strptime(
            date_to, '%Y-%m-%d') - datetime.strptime(date_from, '%Y-%m-%d')).days/max_period_days) + 1
        periods_list = pd.date_range(
            start=date_from, end=date_to, periods=periods_num).tolist()
    else:
        raise Exception("Wrong max_period_days number.")
    return periods_list


def get_pse_data(url_base, periods_list):
    '''
    Download data from website (www.pse.pl). Url_base is filled with dates from periods_list, 
    then data is downloaded and concatenated into one dataframe. Returns dataframe.
    '''
    for i in range(len(periods_list)-1):
        if i == 0:
            url_list = url_base.format(periods_list[i].strftime(
                '%Y%m%d'), periods_list[i+1].strftime('%Y%m%d'))
            df = pd.read_csv(url_list, sep=';', encoding='cp1250')
        else:
            url_list = url_base.format(
                (periods_list[i]+timedelta(days=1)).strftime('%Y%m%d'), periods_list[i+1].strftime('%Y%m%d'))
            df = pd.concat(
                [df, pd.read_csv(url_list, sep=';', encoding='cp1250')], ignore_index=True)
    return df


def get_find_variables(find='table', find_id='footable_kontrakty_godzinowe'):
    '''
    Set variables to scrape object from web. Default find='table', find_id='footable_kontrakty_godzinowe'.
    Returns list in format [find,find_id].
    '''
    find_variables = [find, find_id]
    return find_variables


def check_tge_date_conditions(date_from, date_to):
    '''
    Check if date_from is above todays date minus 3 months and if date_from is below or equal date_to. 
    Dates should be in format YYYY-MM-DD. Returns boolean.
    '''
    min_date = date.today() - relativedelta(months=3)
    min_date_condition = min_date < datetime.strptime(
        date_from, '%Y-%m-%d').date()
    date_order_condition = datetime.strptime(
        date_from, '%Y-%m-%d') <= datetime.strptime(date_to, '%Y-%m-%d')
    return min_date_condition and date_order_condition


def get_data_tge(dates, url_base, find, find_id):
    '''
    Generator which scrape data from website. In a loop url_base is filled with dates, then data is downloaded from filled url_base.
    Find and find_id are used to select properly object in the website. Yields soup.find(find, id=find_id).

    If data is scraped from https://tge.pl/energia-elektryczna-rdn dates has to contain only dates from last 3 months.
    '''
    for date in dates:
        url_tge = url_base.format(date)
        page = requests.get(url_tge)
        soup = BeautifulSoup(page.text, 'lxml')
        soup_find = soup.find(find, id=find_id)
        yield soup_find


def get_header(table, *args, **kwargs):
    '''
    Returns list with all headers available in table text. Other arguments are used in table.find_all(args, kwargs).
    '''
    header = []
    for i in table.find_all(args, kwargs):
        title = i.text
        header.append(title)
    return header


def create_one_header(header_top, header_bottom):
    '''
    Returns list with properly prepared header for dataframe. Function should be used if table has two-row header.
    Values from upper header are taken and joined with every duplicated value from bottom header. 
    Non duplicated values are added to list but are not joined with upper header values.
    '''
    header = ['Data']
    header.append(header_bottom[1])
    duplicates_join = ((x, y) for x in header_top for y in (
        item for item, count in collections.Counter(header_bottom).items() if count > 1))
    for top, bottom in duplicates_join:
        header.append(top + ' - ' + bottom)
    return header


def create_own_header(*args):
    '''
    Returns list with words definied by user.
    '''
    header = [column_name for column_name in args]
    return header


def fill_tge_dataframe(header, dates, gen_tge_data, statistics=False, table_find_all='tr', row_find_all='td', row_min=2, row_max=26):
    '''
    Creates dataframe with columns in header list. Gen_tge_data has to be generator which scrape data from website. 
    Dates has to be list with the same values as used in gen_tge_data.
    If statistics is True, whole table is scraped (with statistics in the end of table), default statistics is False.
    Table_find_all, row_find_all, row_min, row_max are arguments used to extract data from html code.
    Returns dataframe.
    '''
    df = pd.DataFrame(columns=header)
    if statistics:
        row_max = None
    for date, table in zip(dates, gen_tge_data):
        for j in table.find_all(table_find_all)[row_min:row_max]:
            row_data = j.find_all(row_find_all)
            row = [i.text.strip() for i in row_data]
            row.insert(0, date)
            length = len(df)
            df.loc[length] = row
    return df


def save_to_csv(dataframe, name, folder_path=None):
    '''
    Saves dataframe to csv file. Name is the string of new created file. 
    Folder_path is the localization where to save the dataframe.
    '''
    if folder_path:
        dataframe.to_csv(os.path.join(folder_path, name),
                         index=False, encoding='utf-8')
    else:
        dataframe.to_csv(name, index=False, encoding='utf-8')


@click.command()
@click.option('--number', '-n', type=int, required=True, prompt="Select one number from the list below to download table: \n 1 - Praca KSE - Wielkości podstawowe  \n 2 - Praca KSE - Generacja mocy Jednostek Wytwórczych \n 3 - TGE RDN - Kontrakty godzinowe \n", help="Paste 1 or 2 or 3")
@click.option('--date_from', '-df', type=str, required=True, prompt="Enter the start date in format YYYY-MM-DD for data download\n", help="Paste date in format YYYY-MM-DD")
@click.option('--date_to', '-dt', type=str, required=True, prompt="Enter the end date in format YYYY-MM-DD for data download\n", help="Paste date in format YYYY-MM-DD")
@click.option('--folder_path', '-fp', type=str, default='', required=False, show_default=True, prompt="Paste directory where to save the file (optional)\n", help="Paste folder path or click enter to skip.")
@click.option('--statistics', '-s', type=bool, required=False, is_flag=True, show_default=True, prompt="Do you want to download statistics (only for the 3rd option)?\n", help="Paste Y or n or click enter to skip.")
def download_data(number, date_from, date_to, folder_path=None, statistics=False):
    """ 
    Main function to download data from the source, prepare the data and save it to the csv file.\n
    Parameter number is used to select source of the data. It has to be integer between 1 and 3, where: \n 
        1 - Praca KSE - Wielkości podstawowe \n 
        2 - Praca KSE - Generacja mocy Jednostek Wytwórczych \n
        3 - TGE RDN - Kontrakty godzinowe \n
    Parameter date_from definies start date of data period. It has to be in format YYYY-MM-DD.\n
    Parameter date_to definies end date of data period. It has to be in format YYYY-MM-DD.\n
    Parameter folder_path is used to definie path where the csv file has to be saved. Default is the current working directory.\n
    Parameter statistics is useful only for option 3 - TGE RDN - Kontrakty godzinowe, for others options it has no impact.\n
    If parameter statistics is True, Min, Max, Sum values shown in the bottom of the table are downloaded. Default is False.
    """

    url = get_url_base_link(number)
    check_connection(url)

    if folder_path == '':
        folder_path = os.getcwd()

    filename = '_' + date_from + '_' + date_to + '.csv'

    if number == 1:
        if check_dates(date_from, date_to):
            periods = create_data_periods(date_from, date_to, 31)
            data = get_pse_data(url, periods)
            save_to_csv(data, 'PL_WYK_KSE' + filename, folder_path)
        else:
            raise Exception("Wrong dates. Date_from should be below date_to.")
    elif number == 2:
        if check_dates(date_from, date_to):
            periods = create_data_periods(date_from, date_to, 31)
            data = get_pse_data(url, periods)
            save_to_csv(data, 'PL_GEN_MOC_JW_EPS' + filename, folder_path)
        else:
            raise Exception("Wrong dates. Date_from should be below date_to.")
    elif number == 3:
        if check_tge_date_conditions(date_from, date_to):
            periods = create_data_periods(date_from, date_to, 1)
            find_variables = get_find_variables()
            first_table = next(get_data_tge(
                periods, url, find_variables[0], find_variables[1]))

            headers_top = get_header(first_table, 'th', colspan="2")
            headers_bottom = get_header(first_table, 'th', align="")
            header = create_one_header(headers_top, headers_bottom)

            table_to_scrape = get_data_tge(
                periods, url, find_variables[0], find_variables[1])
            data = fill_tge_dataframe(
                header, periods, table_to_scrape, statistics=statistics)
            if statistics:
                save_to_csv(data, 'EE_RDN_statistics' +
                            filename, folder_path)
            else:
                save_to_csv(data, 'EE_RDN' + filename, folder_path)
        else:
            raise Exception(
                "Check the dates. Date_from should be below or equal to date_to and only data for past 3 months is available.")
    else:
        raise Exception("Choose number from 1 to 3.")

    click.echo('File saved in ' + folder_path)
