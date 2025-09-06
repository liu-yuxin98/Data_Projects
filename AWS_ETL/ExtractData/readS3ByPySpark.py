from pyspark.sql import SparkSession
import boto3

# --- Config ---
aws_profile = "yuxinIAM01SSO"
aws_region = "ap-southeast-2"
bucket_region = "ap-southeast-1"  # actual bucket region
bucket = "etlgoods123"
key = "goods_20250906.csv"
s3_path = f"s3a://{bucket}/{key}"
# --------------

# Create a boto3 session to get temporary SSO credentials
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
credentials = session.get_credentials().get_frozen_credentials()

# Start Spark session
spark = (
    SparkSession.builder
    .appName("ReadS3CSV")
    .getOrCreate()
)

# Set S3A configuration for Spark to use temporary credentials
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", credentials.access_key)
hadoop_conf.set("fs.s3a.secret.key", credentials.secret_key)
hadoop_conf.set("fs.s3a.session.token", credentials.token)
hadoop_conf.set("fs.s3a.endpoint", f"s3.{bucket_region}.amazonaws.com")

# Read CSV from S3 into Spark DataFrame
df = spark.read.option("header", True).csv(s3_path)

print("Schema of Spark DataFrame:")
df.printSchema()

print("First 5 rows:")
df.show(5)

# Optional: cache for further processing
df.cache()
