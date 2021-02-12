FROM python:3.8

# Create app directory
RUN mkdir /app
WORKDIR /app

# Install app dependencies
COPY src/requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY src /app

EXPOSE 5000
CMD [ "python", "valet.py" ]