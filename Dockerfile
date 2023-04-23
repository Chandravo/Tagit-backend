# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY ./config/requirements.txt .
RUN pip install daphne
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./config /app

USER root

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["sh", "run.sh"]
