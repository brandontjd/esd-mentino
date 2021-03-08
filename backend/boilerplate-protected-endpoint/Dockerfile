FROM python:3.8-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./protected_endpoint.py .
CMD [ "python", "./protected_endpoint.py" ]