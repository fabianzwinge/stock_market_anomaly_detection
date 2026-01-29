# import the Quix Streams modules for interacting with Kafka.
# For general info, see https://quix.io/docs/quix-streams/introduction.html
from quixstreams import Application
from sklearn.ensemble import IsolationForest
import os


from dotenv import load_dotenv
load_dotenv()

app = Application(
    consumer_group="data_producer",
    auto_create_topics=True,
    auto_offset_reset="earliest",
    broker_address="localhost:19092"
)

input_topic = app.topic(name=os.getenv("input"))
output_topic = app.topic(name=os.getenv("output"))

order_quantity_threshold = 25000

def check_order_quantity_threshold_anomaly(df):
    df['order_quantity_threshold_anomaly'] = bool(df['size'] > order_quantity_threshold)
    return df

def main(): 
    streaming_stock_data = app.dataframe(input_topic)
    streaming_stock_data = streaming_stock_data.apply(check_order_quantity_threshold_anomaly)
    streaming_stock_data = streaming_stock_data.filter(lambda row: row['order_quantity_threshold_anomaly'] == True)

    streaming_stock_data.print()

    streaming_stock_data.to_topic(output_topic)

    app.run()

if __name__ == "__main__":
    main()
