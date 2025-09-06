# AWS_ETL

This project demonstrates a local **ETL pipeline** using Python, Pandas, and PySpark to read data from **AWS S3**, transform and clean it locally, and finally load it into **AWS RDS (PostgreSQL)**. The project is designed to show how to work with cloud data locally before deploying a full production pipeline.

---

## Project Structure

```
AWS_ETL/
├── Data/
├── ExtractData/
│   ├── readS3ByPandas.py       # Read data from S3 using Pandas
│   └── readS3ByPyspark.py      # Read data from S3 using PySpark
├── TransformData/              # Scripts to clean and transform data
├── LoadData/                   # Scripts to load data into AWS RDS
```

---

## Step-by-Step Guide

### 1. Install Conda Environment

Create a dedicated environment to ensure all dependencies are compatible:

```bash
conda create -n aws_spark python=3.9
conda activate aws_spark
```

pip install -r requirements.txt
Install required packages:

```bash

```

**Why:** Keeping a separate environment avoids conflicts between Spark, Hadoop, and Python packages.

---

### 2. Create S3 Bucket and Upload File

- Log in to AWS Console and create a bucket (e.g., `etlgoods123`).
- Upload your CSV file (e.g., `goods_20250906.csv`) to the bucket.

**Why:** The pipeline reads data from S3, simulating real-world cloud storage access.

---

### 3. Refresh AWS Credentials Locally if you already have aws credentials set up locally

If you are using **AWS SSO**, refresh your credentials:

```bash
aws sso login --profile yuxinIAM01SSO
```

**Why:** Temporary SSO credentials are needed to access S3 programmatically.

---

### 3. If you don't have aws sso set up locally you need to set it up

A brief summary for aws sso set up
1 insatll AWS CLI locally: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
2 Config AWS SSO profile
`bash
    aws configure sso
    `
you should input the correct value for setting up
This creates a profile in ~/.aws/config
3 login and refresh sso Token
4 to verify your credentials
`bash
    aws s3 ls --profile yuxinIAM01SSO(ProfileName)
    `
Reference:https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html
**Why:** Set up AWS SSO so that you can interact with aws sdk.

---

### 4. Read Data from S3 with Pandas

Activate your environment:

```bash
conda activate aws_spark
```

Run:

```bash
python ExtractData/readS3ByPandas.py
```

**What it does:**

- Uses **boto3** and **s3fs** to read the CSV directly from S3 into a Pandas DataFrame.
- Allows quick local exploration and basic transformation of the data.

**Why:** Pandas is convenient for small to medium datasets and quick prototyping.

---

### 5. Check Spark and Hadoop Versions

Make sure your environment has compatible versions:

```python
import pyspark
pyspark.__version__   # should be 4.0.0

# Check Hadoop version (from terminal)
hadoop version       # should match Spark-Hadoop compatibility
```

**Why:** Version mismatch can cause `ClassNotFoundException` or S3 access errors.

---

### Launching PySpark (Optional)

You **do not need** to start an interactive PySpark shell to run the ETL jobs. The `spark-submit` command automatically starts Spark and executes your script.

> Optional: If you want to experiment interactively with PySpark, you can start a shell:

1. Open a terminal
2. Activate your conda environment:
   ```bash
   conda activate aws_spark
   ```
3. Start PySpark with required packages:
   `bash
 pyspark --packages org.apache.hadoop:hadoop-aws:3.4.1,com.amazonaws:aws-java-sdk-bundle:1.11.1026
 `
   For running the ETL pipeline scripts, just use spark-submit—no interactive shell is necessary.

---

### 6. Read Data from S3 with PySpark

Run PySpark with the required Hadoop AWS packages:

```bash
spark-submit --packages org.apache.hadoop:hadoop-aws:3.4.1,com.amazonaws:aws-java-sdk-bundle:1.11.1026 readS3ByPyspark.py
```

**What it does:**

- Uses **Spark DataFrame** to read large datasets from S3 efficiently.
- Configures Spark to use temporary SSO credentials.
- Handles distributed data processing, allowing scaling to bigger datasets.

**Why:** PySpark is necessary for high-performance ETL and for datasets too large to fit in memory.

---

### 7. Transform and Clean Data

- Use scripts under `/TransformData` to perform cleaning, type conversions, missing value handling, and derived column calculations.
- Both Pandas and PySpark DataFrames can be used for transformation depending on dataset size.

**Why:** Data cleaning ensures high-quality data for ML or database storage.

---

### 8. Load Data into AWS RDS (PostgreSQL)

- Use Python (`psycopg2` or SQLAlchemy) scripts under `/LoadData` to load transformed DataFrames into RDS.

**Example:**

```python
import psycopg2
conn = psycopg2.connect(
    host="your-rds-endpoint",
    database="dbname",
    user="username",
    password="password"
)
df.to_sql('goods_table', conn, if_exists='replace')
```

**Why:** Storing in RDS allows the data to be queried and used by downstream applications.

---

### Notes

- Always ensure **SSO credentials are valid** before running scripts.
- Use `s3a://` paths in PySpark to access S3.
- Use `--packages` with Spark to include `hadoop-aws` and `aws-java-sdk-bundle`.
- For local development, start with small datasets in Pandas before scaling up with PySpark.

---

This setup allows you to:

1. Read data securely from AWS S3.
2. Transform and clean it locally using Pandas or PySpark.
3. Load it into AWS RDS for further use.
4. Prepare a scalable ETL pipeline for future production deployment.
