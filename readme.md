# Stock Market Anomaly Detection

This project performs real-time stock trade anomaly detection using Kafka for streaming. It consists of a data producer that streams historical or live NASDAQ trade data into a Kafka topic, and an anomaly detector that consumes this data to identify unusual trading activity (e.g., high-volume trades) in real time.

## Prerequisites

- Docker
- Quix CLI (https://quix.io/docs/quix-cli/)

## Quick Start

1. Start the pipelines:
	```
	quix pipeline up
	```
2. In one terminal, start the data producer:
	```
	cd nasdaq_data_producer
	python main.py
	```
3. In another terminal, start the anomaly detector:
	```
	cd anomaly_detector
	python main.py
	```

## Architecture
The producer will stream trade data into Kafka, and the detector will process the stream and print detected anomalies.
```mermaid
%%{ init: { 'flowchart': { 'curve': 'monotoneX' } } }%%
graph LR;
nasdaq_data_producer[fa:fa-rocket nasdaq_data_producer &#8205] --> nasdaq_stocks{{ fa:fa-arrow-right-arrow-left nasdaq_stocks &#8205}}:::topic;
nasdaq_stocks{{ fa:fa-arrow-right-arrow-left nasdaq_stocks &#8205}}:::topic --> anomaly_detector[fa:fa-rocket anomaly_detector &#8205];
anomaly_detector[fa:fa-rocket anomaly_detector &#8205] --> anomalies{{ fa:fa-arrow-right-arrow-left anomalies &#8205}}:::topic;


classDef default font-size:110%;
classDef topic font-size:80%;
classDef topic fill:#3E89B3;
classDef topic stroke:#3E89B3;
classDef topic color:white;
```

## How the App looks like...

The first image shows both topics (nasdaq_stocks and anomalies) listed in the Kafka broker.
![Kafka Topics Overview](img/topics.png)

 The second image shows that an anomaly was detected and output for a transaction.
![Anomaly Detected Example](img/anomaly.png)