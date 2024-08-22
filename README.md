# Crypto Statistics Data Engineering Project

## Technologies used

- **Cloud:** GCP (Google Cloud)
- **Infrastructure as code (IaC):** Terraform
- **Workflow orchestration:** Mage
- **Data Warehouse:** Google BigQuery
- **Data Lake:** Google Cloud Storage
- **Data Transofrmations:** dbt (Data Build Tool)
- **Data Visualizations:** Metabase

## Data Ingestion DAG (Source -> Bucket)
![Data Ingestion DAG](https://github.com/lupusruber/crypto_stats/blob/master/Images/Data%20Ingestion%20DAG.png)

## ETL (Bucket -> DWH)
![ETL DAG](https://github.com/lupusruber/crypto_stats/blob/master/Images/ETL%20Pipeline.png)

## Dashboards
![Dashboard](https://github.com/lupusruber/crypto_stats/blob/master/Images/Dashboard.png.png)

## How to replicate this project?

### 1. Clone the repo
```bash
git clone https://github.com/lupusruber/crypto_stats.git
```

### 2. Create the needed infrastructure
```bash
cd terraform
terraform init
terraform plan
terraform apply
```
### 3. Get Mage and run the pipelines
```bash
docker run -it -p 6789:6789 -v $(pwd):/home/src mageai/mageai /app/run_app.sh mage start [project_name]
```
Copy the pipeline scripts inside the cointainer.

### 4. Get dbt and run the models
For this project dbt cloud was used.
Create a new dbt project and add the models from the repo to the project directory.
Run the command:
```bash
dbt build
```
The staged models and the facts should be part of your big query dataset now.

### 5. Get Metabase and create dashboards
```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
```
Create the dashboards using the data from Big Query.

## Notes
- You need to have a GCS account
- Create a service account and download credentials
- Store credentails in [project_name]/keys/credentials.json, they are used by Terraform, Mage, dbt and Metabase


