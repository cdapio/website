---
title: Finance
hero:
  title: Finance
  second_title: Information Security Analytics and Reporting
  body: "Summary Phasellus tempor magna a tincidunt facilisis. Sed id pulvinar tellus. Nulla et massa lacus."
  link_back_title: « Case studies
  link_back_url: /case-studies
  navigation: false
  background_color: "#404244"
  table:
    - title: Categories
      body: Analytics and business intelligence
    - title: Audience
      body: Business analysts, Data scientists
    - title: Key themes
      body: Code-free transformations, Faster TTM, Lower TCO
    - title: Industry segment
      body: Large enterprise
    - title: Industry
      body: Finance
    - title: Environment
      body: OSS CDAP on-premise
---

### Scenario

The customer, a Fortune 50 financial institution, created a pipeline that aggregates batched data into a 
secured on-premise cluster to create daily aggregates and reports. The current system performed multiple 
transformations, which created new datasets. The customer faced multiple issues: 

* The data pipeline was inefficient, took 6 hours to run, and required manual intervention almost on a daily basis
* Reports were not aligning correctly with day boundaries.
* Any points of failure require reconfiguring and restarting the pipeline, a time-consuming and frustrating task.
* Major setup and development time was needed to add new sources.
* The team was not able to test and validate the pipeline prior to deployment. 
  As a result, testing was conducted directly on the cluster, which is an inappropriate use of resources.  

### CDAP value proposition(s)

The customer’s data development team created independent parallel pipelines that moved the data from SQL Servers into their Hadoop based data lake.

Transformations were performed in-flight with the ability to handle error records.

After completing the initial load, another pipeline fed the data into an aggregation and reporting pipeline.