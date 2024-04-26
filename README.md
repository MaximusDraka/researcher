# Overview
Dissertation project about skill mapping from CV to jobs and courses

# Project aim
The aim is to create a application that suggests courses to follow to improve the 
skills your are missing for your current profile based on your uploaded resume.

This project is the result of a dissertation as a student at the KU Leuven

# Screenshots

# Screenshot of Web app result
![Application user](/screenshots/Webapp-Application-user.JPG?raw=true "Main web app interface")
![Data Analyst](/screenshots/Webapp-Data-Analyst.JPG?raw=true "Top Profile skills")
![Data Engineer](/screenshots/Webapp-Data-Engineer.JPG?raw=true "NER Model monitor")


# Content
This project contains the following aspects:

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
            - charts
            - Basic streamlit components
        - Model log - Dashboard
        - Profile top skills - Dashboard
    - Docker container - Back-end - FAST-API
        - Recommender endpoint
        - Model log endpoint
        - Top skill by profile endpoint

# Tools used to perform this project
- Visual studio Code + Co-pilot plugin
- Anaconda Desktop
- Power BI Desktop
- Python 3.11.8
- NER annotator website
- Neo4J
    - Desktop
    - NeoDash		
    - Browser		
    - Bloom	
- Docker Desktop	
- GIT	
- yEd	

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
This project is not 100% portable, as the Neo4J database is required to run locally outside a docker container.
Although all the code is available to re-create the project.

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