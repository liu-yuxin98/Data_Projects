# 📡 SparkTradeStream

_A real-time financial data streaming demo using Apache Spark Streaming_

---

## 🚀 Overview

This project simulates **real-time financial transactions** (trades, transfers, buys/sells) and processes them with **Apache Spark Streaming**.

It demonstrates a typical **data engineering streaming pipeline**:

- 🏦 **Data Generator** → produces synthetic financial transactions over a TCP socket
- 🔌 **Client Tester** → verifies that the socket server works
- ⚡ **Spark Streaming Client** → consumes the stream, parses JSON transactions, and runs live analytics

---

## 📂 Project Structure

```
SparkTradeStream/
│
├── financial_data_generator.py      # Generates dummy financial transactions
├── financial_data_server.py         # TCP server that streams the transactions
├── spark_client.py                  # Spark Streaming job to process the stream
├── socket_client_test.ipynb         # Simple socket client to test connection
├── spark_streaming_client.ipynb     # Spark Streaming job to process the stream, However it only success the first time running,
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Ignore common files
└── README.md                        # Project documentation
```

---

## ⚙️ Setup Instructions

### 1 Clone the Repository

```bash
git clone https://github.com/liu-yuxin98/Data_Projects/SparkTradeStream.git
cd SparkTradeStream
```

### 2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3 Start the Financial Data Server

The server generates random financial transactions and streams them over TCP port **9999**.

```bash
python financial_data_server.py
```

**Expected output:**

```
🚀 Launching Financial Data Server (Standalone Mode)
📡 Financial data server listening on 127.0.0.1:9999
⏳ Waiting for client to connect...
```

### 4 Test the Stream with a Simple Client

Open **`socket_client_test.ipynb`** in Jupyter.

It connects to `127.0.0.1:9999` and prints raw JSON transactions, for example:

```json
{
  "transaction_id": "8af17512-2dfd-44bf-999a-0b4bb019a840",
  "timestamp": "2025-09-03T20:57:16.482273",
  "account_id": "ACC_64283",
  "transaction_type": "SELL",
  "symbol": "AMZN",
  "quantity": 3473,
  "price": 3521.3,
  "total_amount": 12229474.9,
  "currency": "JPY",
  "exchange": "NYSE",
  "customer_segment": "INSTITUTIONAL"
}
```

### 5 Run the Spark Streaming Client

Run **`spark_client.py`**.

This code:

- Initializes a **Spark StreamingContext**
- Connects to the TCP socket (`localhost:9999`)
- Reads each line of JSON and parses it into structured fields
- Performs simple analytics, e.g., counting transactions by type

**Example output:**

```
=== Transaction Counts by Type (last 5 sec) ===
BUY: 3
SELL: 5
TRANSFER: 2
```

---

## 🧠 How It Works

- **📊 Data Generator** (`financial_data_generator.py`)  
  Produces random trades with fields like `transaction_id`, `timestamp`, `symbol`, `price`, `quantity`, etc.

- **🖥️ Server** (`financial_data_server.py`)  
  Opens a TCP socket on port **9999** and continuously streams JSON transactions.

- **🔍 Client Tester** (`socket_client_test.ipynb`)  
  Verifies the server by printing raw JSON messages.

- **⚡ Spark Client** (`spark_streaming_client.ipynb`)  
  Uses Spark Streaming to connect to the socket, transform JSON into DataFrames, and perform streaming analytics.

---

## 🛠️ Tech Stack

- 🐍 Python (socket programming)
- ⚡ Apache Spark (PySpark, Streaming)
- 📓 Jupyter Notebooks

---

## 🎯 Purpose

This project is designed for:

- Learning **Spark Streaming** basics
- Understanding how **real-time data pipelines** work
- Serving as a **data engineering portfolio project**

---

## ✨ Future Enhancements

- Solving current Bugs:
  - When run spark_streaming_client.ipynb it always get issues, need to reatrt financial_data_server.py
- Save parsed data to a **data lake** (S3/HDFS)
- Switch to **Structured Streaming** instead of DStreams
- Add **real-time dashboards** with Spark + Kafka + Grafana

---
