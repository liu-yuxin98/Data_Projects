from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
import threading

def stop_streaming(ssc, timeout):
    def stop():
        print("Stopping streaming context...")
        ssc.stop(stopSparkContext=False, stopGraceFully=True)
        print("Streaming context stopped.")
    threading.Timer(timeout, stop).start()

if __name__ == "__main__":
    # Create SparkContext and StreamingContext (batch interval 5s)
    sc = SparkContext("local[2]", "FinancialDataStream")
    ssc = StreamingContext(sc, 5)

    # Connect to the TCP server
    lines = ssc.socketTextStream("127.0.0.1", 9999)

    # Parse JSON lines
    transactions = lines.map(lambda line: json.loads(line))

    # Example: count number of transactions per transaction_type
    counts = transactions.map(lambda tx: (tx["transaction_type"], 1)) \
                         .reduceByKey(lambda a, b: a + b)

    counts.pprint()

    amounts = transactions.map(lambda tx: (tx["transaction_type"], tx["total_amount"])) \
                          .reduceByKey(lambda a, b: a + b)
    amounts.pprint()

    stop_streaming(ssc, timeout=40)
    
    # Start streaming
    ssc.start()
    ssc.awaitTermination()


