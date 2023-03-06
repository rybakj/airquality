import ezgmail
from datetime import datetime


def send_email(
        recipients_dict,
        attachments,
        credentials_file,
        success,
        cc = None
):

    now = datetime.now()
    date_year = now.strftime("%d%m%y")
    date_year_full = now.strftime("%d-%m-%Y")

    if success == True:
        subject_email = f'Air quality {date_year}'
        text_email = f'Air quality for date {date_year_full} \n \n Code link: {recipients_dict["github_link"]} \n Google drive link: {recipients_dict["gdrive_link"]}'
    else:
        subject_email = "FAILED to get the data"
        text_email = f'Failed to obtain air quality for date {date_year_full}'


    ezgmail.init(credentialsFile=credentials_file)
    ezgmail.send(recipients_dict["recipient"], subject_email, text_email, attachments, cc = cc)

    return()

if __name__ == "__main__":

    send_email(
        recipient=recipients_dict["recipient"],
        attachments=["../../paper.pdf"],
        credentials_file= "../../credentials.json"
    )