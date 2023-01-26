    CLI Fetch_data_TGE_PSE
    
    To use this CLI you have to type "fetch_data_tge_pse" in terminal.
    After it, the text will be shown and you have to choose number of data source, date from, date to
    and optionally path where the file will be saved and if the statistics Min,Max,Sum have to be downloaded (only for TGE).
    Dates have to be in YYYY-MM-DD format.
    Usage examples are shown in the files "usage_example_1.png and "usage_example_2.png" 

    Fetch_data_tge_pse launches the function download_data, which is the main function which applies other functions 
    in proper order. 

    Download_data is the main function to download data from the source, prepare the data and save it to the csv file.
    Parameter number is used to select source of the data. It has to be integer between 1 and 3, where: 
        1 - Praca KSE - Wielkości podstawowe
        2 - Praca KSE - Generacja mocy Jednostek Wytwórczych
        3 - TGE RDN - Kontrakty godzinowe
    Parameter date_from definies start date of data period. It has to be in format YYYY-MM-DD.
    Parameter date_to definies end date of data period. It has to be in format YYYY-MM-DD.
    Parameter folder_path is used to definie path where the csv file has to be saved. Default is the current working directory.
    Parameter statistics is useful only for option 3 - TGE RDN - Kontrakty godzinowe, for others options it has no impact.
    If parameter statistics is True, Min, Max, Sum values shown in the bottom of the table are downloaded. Default is False.