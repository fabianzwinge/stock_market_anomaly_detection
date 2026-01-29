# import the Quix Streams modules for interacting with Kafka.
# For general info, see https://quix.io/docs/quix-streams/introduction.html
# For sources, see https://quix.io/docs/quix-streams/connectors/sources/index.html
from quixstreams import Application
from quixstreams.sources import Source

import os
import glob
import pandas as pd
import tqdm
import json


from dotenv import load_dotenv
load_dotenv()

app = Application(
    consumer_group="data_producer",
    auto_create_topics=True,
    broker_address="localhost:19092"
)

topic = app.topic(name=os.getenv("output"))

def main():

    with app.get_producer() as producer:
        files = glob.glob('nasdaq_data/*trades.csv.zst')
        files.sort()

        for file_path in tqdm.tqdm(files):
            print(f'Reading file: {file_path}')

            data = pd.read_csv(file_path, compression='zstd')

            #print(data.head())

            for _, row in data.iterrows():
                trade = row.to_dict()

                json_data = json.dumps(trade) 

                # publish
                producer.produce(
                    topic=topic.name,
                    key=trade['symbol'],
                    value=json_data,
                )

        print("Finished publishing all data.")

if __name__ == "__main__":
    main()
