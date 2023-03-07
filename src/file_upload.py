import os
import ast
import requests
import json


def load_json_file(filename):
    '''
    Load json file from the specified path/filename

    :param filename: path to the file
    :return: loaded data (in dictionary)
    '''
    if os.path.exists(filename):
        f = open(filename)
        data = json.load(f)
    else:
        raise ValueError(f"No {filename} file found in {os.getcwd()}")
    return (data)


def get_refresh_token(secrets_dict):
    '''
    Given a secrets file (dict), obtained a refreshed token for Google API to
    enable data download without manual authentication.

    Inputs:
    - secrets_dict: dictionary containing 'client_id', 'client_secret' and 'refresh_token' as keys.

    Outputs:
    - refreshed token (string)
    '''
    rrr = requests.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            'client_id': secrets_dict["client_id"],
            'client_secret': secrets_dict["client_secret"],
            'refresh_token': secrets_dict["refresh_token"],
            'grant_type': "refresh_token"
        }
    )

    # extract the refreshed token:
    dict_str = rrr.content.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)
    token_refresh = mydata['access_token']

    return (token_refresh)


def upload_file(token_refresh,
                parents,
                file_name,
                file_source
                ):
    '''
    Using a given token, upload a file_source file to Goodgle drive, naming it "file_name",
    inside a folder "parents"

    :param token_refresh: token for Google drive API
    :param parents: (list) or None - folder inside which to save the file
    :param file_name: how to call the saved file (string)
    :param file_source: path + name if the file to upload
    :return: status code of the upload request (<300 = success, (300, 399) = redirect, >=400 = error)
    '''
    headers = {"Authorization": "Bearer " + token_refresh}
    para = {
        "name": file_name,
        "parents": parents
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open(file_source, "rb")
    }

    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        # 'https://www.googleapis.com/oauth2/v4/token',
        headers=headers,
        files=files
    )

    return (r.status_code)


def extract_secrets(token_file, client_secrets_file):
    '''
    From specified files, extract secrets needed to authenticate Google drive API
    (and to obtain a refreshed token)

    :param token_file: file path (json file)
    :param client_secrets_file: file path (json file)
    :return: dictionary with keys 'client_id', 'client_secret', 'refresh_token'
    '''

    token_data = load_json_file(token_file)
    csecrets_data = load_json_file(client_secrets_file)

    secrets_dict = dict()
    secrets_dict["client_id"] = csecrets_data["installed"]["client_id"]
    secrets_dict["client_secret"] = csecrets_data["installed"]["client_secret"]
    secrets_dict["refresh_token"] = token_data["refresh_token"]

    return (secrets_dict)


def gdrive_upload(
        file_source, file_name,
        token_file, secrets_file,
        parents=None
    ):
    '''
    Upload a specified file to Google Drive

    :param file_source: path + name of a file
    :param file_name: name of the file to upload
    :param token_file: link to token file (json)
    :param secrets_file: link to cecrets file (json)
    :param parents: list of parent folders (for GDrive)
    :return:
    '''

    # Get credentials/secrets in dictionary
    secrets_dict = extract_secrets(token_file, secrets_file)
    # refresh token
    token_refresh = get_refresh_token(secrets_dict)

    # upload a given file to Gdrive
    request_result = upload_file(token_refresh, parents = parents,
                file_name=file_name, file_source=file_source)

    return (request_result)


if __name__ == "__main__":

    file_source = "./paper.pdf"
    file_name = "new_sample_app4.pdf"
    token_file = "token.json"
    secrets_file = "client_secrets.json"
    parents = ['1STuaun4Z422N5OZ30TrO7U0xXzoEPUBQ']

    request_result = gdrive_upload(
        file_source, file_name,
        token_file, secrets_file,
        parents
    )

    if request_result < 300:
        result_msg = "Success"
    else:
        result_msg = "Failed to upload a file - request.post rejected"
    print(result_msg)

# SCOPES = ['https://www.googleapis.com/auth/drive.file']
