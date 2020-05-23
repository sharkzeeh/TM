import requests
import os


if not os.path.exists('data'):
    os.mkdir('data')
LINK = "143l8ldjqPUetsl3gPblVsT8XBYdd4yag"


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def download_file_from_web_server(url, destination):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    response = requests.get(url, stream=True)
    save_response_content(response, os.path.join(destination, local_filename))
    return local_filename


#  TODO Add progress bar
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    print('here')
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

# download_file_from_google_drive(LINK, 'data/data.json')



