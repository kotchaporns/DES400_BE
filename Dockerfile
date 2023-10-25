#pulling python image
FROM python:3



#switch working directory
WORKDIR /app

#copy requirements file into image
COPY requirements.txt requirements.txt

#install dependencies and packages in requirements file
RUN pip3 install -r requirements.txt

#copy every content from the local file to the image
COPY . .

#configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

CMD ["python3", "-m", "flask", "run","--host=0.0.0.0"]