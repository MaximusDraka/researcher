# Overview
Dissertation project about skill mapping from CV to jobs and courses.

# Project aim
The aim is to create a application that suggests courses to follow to improve the 
skills your are missing for your current profile based on your uploaded resume.

Currently the following profiles are part of this project: Data engineer, Data analyst and Data scientist.

This project is the result of a dissertation as a student at the KU Leuven.

# Screenshot of Web app result
![Application user](/screenshots/Webapp-Application-user.JPG?raw=true "Main web app interface")
![Data Analyst](/screenshots/Webapp-Data-Analyst.JPG?raw=true "Top Profile skills")
![Data Engineer](/screenshots/Webapp-Data-Engineer.JPG?raw=true "NER Model monitor")

# Setup - Python app
- Download full project
- create pip or conda environment based on requirements.txt
- Create Neo4J database from /data/database/profile-kb.dump 
    - Option A : Local Neo4J desktop - Configure neo4J database to use local fixed IP - See /screenshots for example
    - Option B : Neo4J Aura
- create .env file in the root folder DB_USERNAME, DB_PASSWORD, DB_PORT, DB_URI- 
- Run python main.py --help or notebooks/demo/app.ipynb

# Setup - Web app
- Download /app
- create .env file in the /app/back folder DB_USERNAME, DB_PASSWORD, DB_PORT, DB_URI, PROJECT_PATH, LOG_FILE, MONITOR_FILE
- Install docker
- Follow instructions under /docs/docker-commands.txt

# Content
This project based on Python contains the following aspects:

- Ontology
- Knowledge base - Creation of Neo4J database
    - Profiles -> [HAS score] -> Skill
- Utility modules
    - Knowledge base
    - Neo4J + graph + connection + query library
    - Logger + Monitor
    - PDF tools
    - Spacy
- Data processing 
    - Scrapers of multiple websites (CV, Jobs and courses)- 
    - Pre-annotate scraped data with a spacy matcher based on a knowledge base
    - Transform CSV data to https://tecoholic.github.io/ner-annotator/ format, extract tags and build final data set to import into the database
    - Pre-train NER model using Goolge colab GPU processing
- Spacy workflow starting from the annotated json data = assets
    - Info
    - download model
    - package model
    - validate data
    - Split data into train, test and evaluate spacy files
    - Train
    - Evaluate
    - Spacy-streamlit vizualizer: Model and data
    - Display model metrices and compare with evaluation resuls
- Creation of Neo4J database and data records based on scraped data and Knowledge base + calculate Profile-Skill score
- Reporting and dashboarding projects
    - Power BI - Using FAST-API
    - NeoDash using Neo4J database
    - GraphML    
- Notebook demo app /notebooks/demo/app.ipynb
- CLI demo app /main.py
- Web app
    - Docker container - Front-end - Streamlit
        - Upload PDF resume - detect skills - define profile - recommend courses
            - Displacy
            - Altair charts
            - Basic streamlit components
        - Model log - Dashboard
        - Profile top skills - Dashboard
    - Docker container - Back-end - FAST-API
        - Recommender endpoint
        - Model log endpoint
        - Top skill by profile endpoint

# Tools used to perform this project
- Visual studio Code + Co-pilot plugin - 1.88.1
- Anaconda Desktop - 2.6.0
- Power BI Desktop - 2.123.742.0 64-bit
- Python - 3.11.8
- NER annotator website - https://tecoholic.github.io/ner-annotator/
- Local Neo4J
    - Desktop - 5.12.0
    - NeoDash - 2.4.6		
    - Browser - 5.15.0		
    - Bloom	- 2.11.0
- Cloud Neo4J
    - Neo4J Aura
    - https://neodash.graphapp.io/
- Docker Desktop - v24.0.7	
- GIT	
- yEd - 3.23.2	

# Major Python modules used
- Pandas
- Selenium	
- BeatifulSoup
- Spacy	
- Neo4J-drivers	
- NetworkX
- FAST-API
- Streamlit

# Used for analysis
- Google colab - GPU Pre-training NER model
- Open AI - Auto-annotate text

# Disclaimers
All the information you contribute to this repository, including github issues and code samples are public and open.
The data pre-processing is performed with multiple jupyter Notebooks, afterwards a spacy project takes over the NER model training.
This project requires a Neo4J database containing the ontology and available courses, a sample databse can be found as a dump file under /data/database.
All the code is available to re-create the project.

# Jupyter notebooks references
- Create KB in Neo4J based on vocabulary - Only SKILLS and profiles, no links 
    - neo4J/create-kb-db-from-voc.ipynb
- Update Matcher based on skills in DB and save to disk 
    - KB/create_spacy_matcher_from_kb 
    - models/NER/finalized-matcher.pickle
- Scrape data (CSV)
    - Vaia : scraper/vaia/vaia-scraper.ipynb                    
    - Indeed : scraper/indeed/indeed-scraper.ipynb              
    - Livecareer : scraper/livecareer/livecareer-scraper.ipynb  
- Pre-annotate scraped data with spacy matcher (JSON)
    - spacy/spacy-pre-annotate-text-to-file.ipynb 
    - CSV[‘data’] -> JSON 
- Annotate Online = https://tecoholic.github.io/ner-annotator/ (JSON)
- Extract tags to create a final CSV file to import into Neo4J database (CSV)
    - spacy/extract_tags_from annotation.ipynb

# Recommended improvements
- Turn all notebooks into python scripts and add them to the spacy project
- Host Neo4J : https://neo4j.com/cloud/platform/aura-graph-database/