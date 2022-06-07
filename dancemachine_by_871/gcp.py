from google.cloud import storage
import os
from termcolor import colored
from dancemachine_by_871.params import BUCKET_NAME, PROJECT_NAME


def get_urls(input_name):
    # Instantiates a client
    client = storage.Client(project=PROJECT_NAME)
    # Instantiates a bucket
    bucket = client.bucket(BUCKET_NAME)

    videos_fine = [filename.name for filename in list(bucket.list_blobs(prefix='cutted/fine/dance_')) if filename == input_name]

    return videos_fine


def storage_upload(client, name, temp_local_path, rm=False):
    base_path = 'UPLOADED'
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"{base_path}/{name}")
    blob.upload_from_filename(f"{temp_local_path}/{name}")

    print(colored(f"=> video uploaded to bucket {BUCKET_NAME} inside {base_path}/{name}",
                  "green"))

    if rm:  # Remove temp file after uploading
        os.remove(f"{temp_local_path}/{name}")

    '''
    If we need to work with json file instead of secrets we could do the following:
    # add the service secret file locally then add the path to the following line
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/file.json"
    '''