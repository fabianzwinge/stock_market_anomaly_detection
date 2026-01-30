# import the Quix Streams modules for interacting with Kafka.
# For general info, see https://quix.io/docs/quix-streams/introduction.html
from quixstreams import Application
from sklearn.ensemble import IsolationForest
import os
import numpy as np


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

is_trained = False
prices = []
if_price_model = IsolationForest(
    contamination=0.01,
    random_state=42,
    n_estimators=1000
)

def check_price_anomaly(df):
    global is_trained
    curr_price = df['price']
    prices.append(float(curr_price))

    if len(prices) < 1000:
        df['price_anomaly'] = False
        return df
    
    prices_normalized = (np.array(prices) - np.mean(prices)) / np.std(prices)
    prices_reshaped = prices_normalized.reshape(-1, 1)

    if len(prices) % 1000 == 0: #retrain every 1000 samples
        if_price_model.fit(prices_reshaped)
        is_trained = True

    if not is_trained:
        df['price_anomaly'] = False
        return df

    curr_price_normalized = (curr_price - np.mean(prices)) / np.std(prices)
    score = if_price_model.decision_function([[curr_price_normalized]])

    df['price_anomaly'] = bool(score[0] < 0)  # Negative scores indicate anomalies
    
    return df

def aggregate_anomalies(df):
    anomalies = []
    if df['order_quantity_threshold_anomaly']:
        anomalies.append('order_quantity_threshold_anomaly')
    if df['price_anomaly']:
        anomalies.append('price_anomaly')
    
    df ['anomalies'] = anomalies if anomalies else None
    return df

def main(): 
    streaming_stock_data = app.dataframe(input_topic)
    streaming_stock_data = (streaming_stock_data
        .apply(check_order_quantity_threshold_anomaly)
        .apply(check_price_anomaly)
        .apply(aggregate_anomalies)
    )

    streaming_stock_data = streaming_stock_data.filter(lambda row: row['anomalies'] and len(row['anomalies']) > 0)
    streaming_stock_data.print()
    streaming_stock_data.to_topic(output_topic)

    app.run()

if __name__ == "__main__":
    main()
