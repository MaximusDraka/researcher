# reduced python as base image
FROM python:3.10-slim-buster 

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . . 

# pip install dependencies
#--no-cache-dir
RUN pip install -r requirements.txt

# expose port 8501
EXPOSE 8501 

# command that is run when container is started
CMD ["streamlit", "run", "./app.py"]