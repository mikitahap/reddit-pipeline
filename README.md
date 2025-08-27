# Reddit API ETL Pipeline

This repository contains a multi-stage ETL pipeline for Reddit API data.

## Description

## Key Features

1. **Data Extraction (ETL)**
   - Pulls Reddit posts from the API in near real-time.
   - Supports configurable queries for specific subreddits.

2. **Data Processing & Classification**
   - Preprocesses textual data from Reddit posts.
   - Classifies posts using a **Joblib ML model**.
   - Calculates metrics like average post scores and top words by category.

3. **Data Storage**
   - Stores processed posts in a **PostgreSQL database**.
   - Enables easy querying and analysis.

4. **Visualization & Analytics**
   - Interactive **Streamlit dashboard** showing:
     - Latest posts table
     - Category distribution
     - Average scores per category
     - Top words by category

5. **Orchestration & Automation**
   - Apache Airflow DAGs handle ETL scheduling.
   - Modular architecture for easy pipeline extension.

6. **Containerization & Reproducibility**
   - Docker Compose sets up PostgreSQL, Airflow, and Streamlit.
   - Ensures consistent environments across machines.


## How to use the pipeline

Create a .env file and fill it with your configuration:

```bash
nano .env
```
Example .env file:

```bash
USERNAME=Example_User
USER_PASSWORD=Strong_Password
CLIENT_ID=ID12345
CLIENT_SECRET=sEcReTkEy
```

Run using Docker Compose:

```bash
docker-compose up
```

Apache Airflow Web UI will be available at http://localhost:8081/

Streamlit Web UI will be available at http://localhost:8501/

Project structure (in progress)

```bash
/docker-compose.yml # Docker setup
/scripts
    /extract.py   # Extraction scripts and raw data
    /transform.py # Data cleaning and transformation scripts
    /load.py      # Loading scripts to destination (DB, etc)
    /init_database.py   # Database initialization scripts
    /classification_train.py # ML model training script
/dags
    /pipeline_dag.py # dag file for scheduling
/streamlit_app
    /app.py # script for streamlit visualization
/requirements.txt # Project dependencies
/.gitignore # git ignored files and directories
/README.md        # This file
```
