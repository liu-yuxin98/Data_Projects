from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col, explode
import pyspark.sql.functions as f

from pyspark.sql import SparkSession

def main():
    # Initialize SparkSession
    spark = SparkSession.builder.appName("ETL Pipeline").getOrCreate()
    sc = spark.sparkContext  # Get SparkContext to use RDD methods

    # Read text file
    rdd = sc.textFile("../Data/WordData.txt")

    # -------------------------
    # Transformations
    # -------------------------

    # 1. Filter: remove empty lines
    non_empty = rdd.filter(lambda line: line.strip() != "")

    # 2. flatMap: split each line into words
    words = non_empty.flatMap(lambda line: line.split(" "))

    # 3. map: map each word to (word, 1)
    word_pairs = words.map(lambda w: (w.lower().strip(",.!?"), 1))

    # 4. reduceByKey: count occurrences
    word_counts = word_pairs.reduceByKey(lambda a, b: a + b)

    # 5. filter: keep only words with count > 1
    frequent_words = word_counts.filter(lambda x: x[1] > 1)

    # 6. groupByKey: group counts (not always efficient, but for demo)
    grouped = word_pairs.groupByKey().mapValues(list)

    # -------------------------
    # Actions
    # -------------------------

    print("\n--- Word Counts ---")
    for word, count in word_counts.take(10):  # show first 10
        print(f"{word}: {count}")

    print("\n--- Frequent Words (count > 1) ---")
    for word, count in frequent_words.collect():
        print(f"{word}: {count}")

    print("\n--- Grouped by Key Example ---")
    for word, values in grouped.take(5):
        print(f"{word}: {values}")

    # Stop Spark
    input("\nPress Enter to exit...")  # pause to keep Spark UI open
    spark.stop()

if __name__ == "__main__":
    main()
