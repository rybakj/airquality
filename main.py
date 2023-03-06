from src.download_data import download_and_save_data
from src.file_upload import gdrive_upload, load_json_file
from src.send_email import send_email


if __name__ == "__main__":

    # set key access files
    token_file = "./creds/token.json"
    secrets_file = "./creds/client_secrets.json"
    credentials_file = "./creds/gmail/credentials.json"
    recipients_file = "./creds/gmail/links_recipients.json"

    recipients_dict = load_json_file(recipients_file)
    # 1. Download data
    file_name, sample_file_name, success = download_and_save_data(
        link="http://api.waqi.info/map/bounds/?token=c1032bdbcd4672eaffbceb3fba8ac94c99591e13&latlng=70.4,-27.6,19.4,123.7",
        name_csv="Air quality data"
    )
    
    # 2. upload data
    if success == True:
        parents = ['1STuaun4Z422N5OZ30TrO7U0xXzoEPUBQ']

        request_result = gdrive_upload(
            file_source =  f"./data/{file_name}",
            file_name = file_name,
            token_file = token_file,
            secrets_file = secrets_file,
            parents = parents
        )
    else:
        pass

    # 3. if success send email with data, otherwise send error email
    if (success == True) & (request_result < 300):
        print("Success")

        send_email(
            recipient=recipients_dict["recipient"],
            attachments=[f"./data/{sample_file_name}"],
            credentials_file = credentials_file,
            success = True,
            cc = None
        )

    else:

        send_email(
            recipient=recipients_dict["maintainer"],
            cc = recipients_dict["recipient"],
            attachments=None,
            credentials_file = credentials_file,
            success = False,
        )