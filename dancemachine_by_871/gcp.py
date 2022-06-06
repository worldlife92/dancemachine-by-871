from google.cloud import storage
import os
from termcolor import colored
from dancemachine_by_871.params import BUCKET_NAME, PROJECT_NAME

def storage_upload(client, name, temp_path, rm=False):
    gcc_path = 'UPLOADED'
    storage_location = f"{gcc_path}/{name}"

    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(storage_location)
    blob.upload_from_filename(f"{temp_path}/{name}")

    print(colored(f"=> video uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))

    if rm:  # Remove temp file after uploading
        os.remove(f"{temp_path}/{name}")

    '''
    If we need to work with json file instead of secrets we could do the following:
    # add the service secret file locally then add the path to the following line
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/file.json"
    '''
