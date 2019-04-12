---
title: Telecommunications
hero:
  title: E-commerce
  second_title: In-flight brand sentiment analysis of the Twitter Firehose
  body: "Summary Phasellus tempor magna a tincidunt facilisis. Sed id pulvinar tellus. Nulla et massa lacus."
  link_back_title: « Case studies
  link_back_url: /case-studies
  navigation: false
  background_color: "#404244"
  table:
    - title: Categories
      body: Analytics and business intelligence
    - title: Audience
      body: Java developers
    - title: Key themes
      body: Code-free transformations, Faster TTM, Lower TCO
    - title: Industry segment
      body: Large enterprise
    - title: Industry
      body: E-commerce
    - title: Environment
      body: OSS CDAP on-premise
---

### Scenario

A Fortune 500 e-commerce company built a data pipeline that ingested their Twitter stream in real-time. 
The data was cleansed and transformed prior to conducting multi-dimensional aggregation and sentiment 
analysis on marketing campaigns based on tweets. The results were updated twice daily to HBase. However, 
the legacy pipeline suffered on two fronts: first, latency in the existing pipeline delayed the decision 
making process. Second, the existing data movement process proved to be costly in time and money.

### CDAP value proposition(s)

The company’s in-house team of Java developers built a real-time pipeline in two weeks using the drag-and-drop visual interface in CDAP.

They developed a sentiment analysis transform using the API and then included it in the pipeline. Further, they added multidimensional 
aggregations without needing to write code using the Cube Plugin as a sink.