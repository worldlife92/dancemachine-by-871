from google.cloud import storage

PROJECT_NAME="wagon-data-bootcamp-871"
BASE_URL = "https://storage.googleapis.com"
BUCKETNAME = "dance_871"

def get_urls(input_name):
    # Instantiates a client
    client = storage.Client(project=PROJECT_NAME)
    # Instantiates a bucket
    bucket = client.bucket(BUCKETNAME)

    videos_fine = [filename.name for filename in list(bucket.list_blobs(prefix='cutted/fine/dance_')) if filename == input_name ]

    return videos_fine
