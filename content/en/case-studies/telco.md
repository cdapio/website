---
title: Retail
hero:
  title: Telco
  second_title: Encrypting and Data Masking
  body: "Summary Phasellus tempor magna a tincidunt facilisis. Sed id pulvinar tellus. Nulla et massa lacus."
  link_back_title: « Case studies
  link_back_url: /case-studies
  navigation: false
  background_color: "#404244"
  table:
    - title: Categories
      body: EDW offloading, Technology consolidation
    - title: Audience
      body: Java developers
    - title: Key themes
      body: Data mapping and transformation, code-free transformations
    - title: Industry segment
      body: Large enterprise
    - title: Industry
      body: Telco
    - title: Environment
      body: OSS CDAP on-premise
---

### Scenario

The customer, a Fortune 50 company in the Telecom sector, developed a legacy custom data pipeline that 
performed format-preserving encryption and data masking. The pipeline extracted data from Teradata to HDFS, 
performed transformations, and loaded the results back into Teradata on a daily basis. 
This pipeline, built by a third-party service, was operationally unstable and required constant, costly 
intervention to keep it running.

### CDAP value proposition(s)

The self-service, code-free interface allowed the in-house team to reproduce and replace the existing pipeline.

The new process performed the extraction, encryption, masking, and reload to and from Teradata in-flight.

It created a copy of the data on HDFS so the team could run complex ad-hoc queries using Hive.