# Terrorism Data Analysis Pipeline & Interactive Dashboard

An end-to-end data engineering and analytics project that processes terrorism event data, extracts structured information from multiple sources, performs data transformation, stores processed datasets, and visualizes key insights using Tableau.

---

## Project Overview

This project demonstrates a complete data analytics workflow:

- Data ingestion from raw CSV and text files
- Data cleaning and preprocessing
- Entity extraction from unstructured text
- Schema standardization
- Dataset partitioning for efficient analysis
- Cloud storage integration using AWS S3
- SQL-based analytical queries
- Interactive Tableau dashboards for visualization

The project follows a modular pipeline, making it easy to extend for larger datasets or additional analyses.

---

## Project Structure

```text
terrorism-data-analysis/
│
├── src/
│   ├── ingestion/
│   │   ├── csv_cleaner.py
│   │   ├── text_entity_extractor.py
│   │   └── video_metadata_extractor.py
│   │
│   ├── pipeline/
│   │   ├── schema_mapper.py
│   │   └── partition_data.py
│   │
│   └── aws/
│       └── upload_to_s3.py
│
├── analysis/
│   └── queries/
│
├── outputs/
│   ├── query_results/
│ 
└── README.md
```

---

## Features

### Data Cleaning

- Handles inconsistent records
- Removes duplicates
- Standardizes missing values
- Cleans malformed entries

### Entity Extraction

Extracts structured entities such as:

- Country
- City
- Terrorist Organization
- Attack Type
- Target Type
- Casualties
- Date Information

from semi-structured textual datasets.

### Data Transformation

- Schema mapping
- Column normalization
- Data partitioning
- Optimized datasets for querying

### Cloud Storage

- Upload processed datasets to AWS S3
- Organized storage for scalable analytics

### Data Visualization

Interactive Tableau dashboards showing:

- Terror attacks over time
- Geographic distribution
- Most active terrorist organizations
- Casualty trends
- Attack type distribution
- Country-wise statistics

---

# Dashboard Preview

## Overview Dashboards
<br>
<br>
<img width="662" height="702" alt="Screenshot 2026-07-27 at 7 46 08 PM" src="https://github.com/user-attachments/assets/d83ec2a0-6939-4389-ab2e-0eb10fc77f4a" />
<br>
<br>
<img width="686" height="850" alt="Screenshot 2026-07-27 at 7 47 22 PM" src="https://github.com/user-attachments/assets/f9d0e359-cb71-4a90-8ea9-8509f801d074" />
<br>
Links:
<br>
https://public.tableau.com/app/profile/araina.komal.singh/viz/TerrorismAnalysis_17817665222100/Dashboard2
https://public.tableau.com/app/profile/araina.komal.singh/viz/TerrorismAnalysis_17817665222100/Dashboard3



---

## Analysis Performed

The project includes analytical queries such as:

- Total attacks per year
- Attacks in India by year
- Average casualties by country
- Most dangerous terrorist organizations
- High severity attacks
- Top affected cities
- Distribution of attack types

Generated outputs are available inside:

```
outputs/query_results/
```

---

## Tech Stack

### Programming

- Python

### Libraries

- Pandas
- NumPy
- Regex
- CSV
- boto3 (AWS SDK)

### Visualization

- Tableau

### Cloud

- AWS S3

---

## Pipeline 

```text
Raw Data
    │
    ▼
CSV Cleaning
    │
    ▼
Entity Extraction
    │
    ▼
Schema Mapping
    │
    ▼
Data Partitioning
    │
    ▼
AWS S3 Storage
    │
    ▼
SQL Analysis
    │
    ▼
Tableau Dashboard
```





