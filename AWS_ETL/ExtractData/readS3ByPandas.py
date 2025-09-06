import boto3
import pandas as pd

# --- Config ---
aws_profile = "yuxinIAM01SSO"
aws_region = "ap-southeast-2"
bucket = "etlgoods123"
key = "goods_20250906.csv"
s3_path = f"s3://{bucket}/{key}"
# --------------

# Start a session using your SSO profile
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
credentials = session.get_credentials().get_frozen_credentials()

# Construct a s3fs-compatible URL with credentials
# Option 1: pandas can read directly using s3fs + credentials
df = pd.read_csv(
    s3_path,
    storage_options={
        "key": credentials.access_key,
        "secret": credentials.secret_key,
        "token": credentials.token
    }
)

print("First 5 rows:")
print(df.head())
print("Columns:", df.columns)
