import urllib.request, json
import pandas as  pd
from datetime import datetime


def download_and_save_data(
        link,
        name_csv
):
    '''
    Donwload data and save the data and sample data (= head(data)) to ./data folder.


    :param link: http link to the data
    :param name_csv: name of csv - e.g. "Air quality". The date is added automatically to it
    :return: - file_name: name of the full data file
             - sample_file_name: name of sample file
             - success: True if all actions were succesfull, False otherwise
    '''
    try:
        # get current date & time
        now = datetime.now()
        date_time_formatted = now.strftime("%d-%b-%Y %H.%M")

        # get data
        with urllib.request.urlopen(link) as url:
            data = json.load(url)
            data_df = pd.DataFrame(data["data"])
            data_df["station"] = data_df["station"].apply(lambda x: x["name"])

        # form file names
        file_name = f"{name_csv} - {date_time_formatted}.csv"
        sample_file_name = f"Sample {name_csv} - {date_time_formatted}.csv"

        # save to csv
        data_df.to_csv(f"./data/{file_name}")
        data_df.head().to_csv(f"./data/{sample_file_name}")

        success = True
    except:
        # if failure: empty names and success = False
        success = False
        file_name, sample_file_name = None, None

    return (file_name, sample_file_name, success)
