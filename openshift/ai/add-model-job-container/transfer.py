from boto3 import client
from os import getenv, fsencode, listdir, path
from subprocess import call

call(["git", "clone", "https://huggingface.co/instructlab/granite-7b-lab", "/tmp"])

s3 = client("s3",
            endpoint_url=getenv("AWS_S3_ENDPOINT"),
            aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"))

bucket = getenv("AWS_S3_BUCKET")
if bucket not in [bu["Name"] for bu in s3.list_buckets()["Buckets"]]:
    s3.create_bucket(Bucket=bucket)

directory = fsencode('/tmp/granite-7b-lab')
for file in listdir(directory):
    filename = fsdecode(file)
    if filename.endswith(".json") or filename.endswith(".safetensors") or filename.endswith(".model") or filename.endswith(".pdf"):
        with open(path.join(directory, filename), "rb") as f:
            s3.upload_fileobj(f, bucket, f'granite/{filename}')
