FROM python:3.10.4-slim-bullseye

# We don't want to run our application as root if it is not strictly necessary, even in a container.
# Create a user and a group called 'app' to run the processes.
RUN adduser --system --group app

COPY /system/ /app/
COPY requirements.txt ./
COPY config.json /app/


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

# Hand everything over to the 'app' user
RUN chown -R app:app /app

USER app

# Make the directory the working directory for subsequent commands
WORKDIR /app

RUN python3 get_data.py -u