FROM python:3.8-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY gcp-credentials.json ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./bubble_file.py .
CMD [ "python", "./bubble_file.py" ]