import urllib.request, json
import pandas as  pd
from datetime import datetime


def download_and_save_data(
        link,
        name_csv
):
    try:

        now = datetime.now()
        date_time_formatted = now.strftime("%d-%b-%Y %H.%M")

        with urllib.request.urlopen(link) as url:
            data = json.load(url)
            data_df = pd.DataFrame(data["data"])
            data_df["station"] = data_df["station"].apply(lambda x: x["name"])

        file_name = f"{name_csv} - {date_time_formatted}.csv"
        sample_file_name = f"Sample {name_csv} - {date_time_formatted}.csv"

        data_df.to_csv(f"./data/{file_name}")
        data_df.head().to_csv(f"./data/{sample_file_name}")

        success = True
    except:
        success = False
        file_name, sample_file_name = None, None

    return (file_name, sample_file_name, success)
