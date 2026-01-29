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