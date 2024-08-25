from boto3 import client
from os import getenv, listdir, path, makedirs
from subprocess import call

# dir
directory = "/opt/app-root/models/granite-7b-lab"
makedirs(directory)

# download model
call(["git", "clone", "https://huggingface.co/instructlab/granite-7b-lab", directory])
print("model downloaded from huggingface")

s3 = client("s3",
            endpoint_url=getenv("AWS_S3_ENDPOINT"),
            aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"))

# create bucket if not exist
bucket = getenv("AWS_S3_BUCKET")
if bucket not in [bu["Name"] for bu in s3.list_buckets()["Buckets"]]:
    s3.create_bucket(Bucket=bucket)
    print(f"created {bucket} bucket")
else:
    print(f"{bucket} bucket exists already")

# upload models
for filename in listdir(directory):
    f = path.join(directory, filename)
    if path.isfile(f):
        with open(f, "rb") as file:
            s3.upload_fileobj(file, bucket, f"granite/{filename}")
            print(f"uploaded {filename}")
