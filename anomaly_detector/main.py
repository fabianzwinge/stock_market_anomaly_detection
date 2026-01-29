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

def main(): 
    streaming_nasdaq_stock_data = app.dataframe(input_topic)
    streaming_nasdaq_stock_data.print()
    app.run(streaming_nasdaq_stock_data)

if __name__ == "__main__":
    main()
