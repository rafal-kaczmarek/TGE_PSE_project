# Data engineering project

## Installation & setup

1. Make sure you have Python 3.10.6 installed.
2. Clone the repository.
3. Run the following commands in the terminal in order to create and activate virtual environment:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. In order to setup the whole project run the following command:
    ```
    pip install --editable .
    ```
5. In order to launch the app run the following command:
    ```
    fetch_data_tge_pse
    ```

## CLI Fetch_data_TGE_PSE description

To use this CLI you have to type ```fetch_data_tge_pse``` in terminal.
After it, the text will be shown and you have to choose number of data source, date from, date to
and optionally path where the file will be saved and if the statistics Min,Max,Sum have to be downloaded (only for TGE).
Dates have to be in YYYY-MM-DD format. Usage examples are shown in the files "usage_example_1.png" and "usage_example_2.png".

Fetch_data_tge_pse launches the function download_data, which is the main function which applies other functions 
in proper order. 

Download_data is the main function to download data from the source, prepare the data and save it to the csv file.
Parameter ```number``` is used to select source of the data. It has to be integer between 1 and 3, where:
<br>    1 - Praca KSE - Wielkości podstawowe
<br>    2 - Praca KSE - Generacja mocy Jednostek Wytwórczych
<br>    3 - TGE RDN - Kontrakty godzinowe

Other parameters:
<br> - ```date_from``` definies start date of data period. It has to be in format YYYY-MM-DD. 
<br> - ```date_to``` definies end date of data period. It has to be in format YYYY-MM-DD.
<br> - ```folder_path``` is used to definie path where the csv file has to be saved. Default is the current working directory.
<br> - ```statistics``` is useful only for option 3 - TGE RDN - Kontrakty godzinowe, for others options it has no impact.
<br> If parameter statistics is True, Min, Max, Sum values shown in the bottom of the table are downloaded. Default is False.


