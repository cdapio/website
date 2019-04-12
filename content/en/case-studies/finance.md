---
title: Finance
hero:
  title: Finance
  body: "Summary Phasellus tempor magna a tincidunt facilisis. Sed id pulvinar tellus. Nulla et massa lacus."
  link_back_title: « Case studies
  link_back_url: /case-studies
  navigation: false
  background_color: "#404244"
  table:
    - title: Categories
      body: EDW offloaditng, Technology consolidation
    - title: Audience
      body: Data Administrators, Data Analysts, Data Scientists, Engineers
    - title: Key themes
      body: Removal of departmental silos, IT dependency reduction, Extensibility
    - title: Industry segment
      body: SMB
    - title: Industry
      body: Healthcare
    - title: Environment
      body: On-premises
---

### Scenario

The customer, a Health Insurance company, was using Netezza to aggregate and report on multiple dimensions on different health 
care and services. They were looking for alternatives to offload the data from Netezza to reduce the workload for reducing the 
cost. Data Administrators, Data Analysts, Data Scientist and Engineers were operating and supporting the loading, cleansing and 
reporting efforts. They were facing a lot of difficulties in the following 
areas that was hindering their transition into Hadoop:

* Current implementation of moving data into and out of Hadoop was 
error prone and took a lot of effort and time to add new aggregations or reports
* Data Administrator, Data Analyst and Data Engineers were spending a lot of building complex workflows 
and less time on looking at data insights and reports
* Every new report or data source ingestion from Netezza took months to generate
* Due to the health industry regulations, they were not having a reliable solution to track the 
flow of data in and out of cluster
* Integrating and making the data available within Impala was challenging

### CDAP value proposition(s)

Customer was successfully able to extract data from Netezza and other SQL sources, perform complex joins, transformation and load it into distributed file system. They were then able to perform different aggregations and joins to generate the final reports. They were able to load the final report data back into Netezza seamlessly. 

The company’s in-house team of Data Analysts, Data Scientists and Data Engineers built a data pipeline in less than a week using the drag-and-drop visual interface in CDAP. 

They were then able to operationalize (schedule to run on a daily basis) and report on errors in data giving them the visibility that they were looking for. 
Beyond those capabilities, they were able to build pipeline level dashboard that provided them deep insights into how the offloading and report generation process was functioning.