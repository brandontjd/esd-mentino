# The Mentoring Bubble

## Description
In university, ​independent learning is key​. However, students can sometimes face difficulties in certain modules, where new and technical concepts are introduced, and require additional assistance​.

The Mentoring Bubble aims to bridge this gap by providing a marketplace for students to find Bubbles (workshops) where mentors volunteer to guide students through the module, give them tips and reinforce weak concepts.​

## Run locally

### 1. Retrieve GCP credentials
1. Create a new bucket on Google Cloud
2. Copy and paste the `gcp-credentials.json` to ./backend/BubbleFiles/
3. Copy the bucket name

### 2. Retrieve LogDNA Ingestion Key
1. Sign up for LogDNA account
2. Copy the `LogDNA Ingestion key`

### 3. Enable Gmail account
1. Create a Gmail account
2. Copy the email and password
3. Allow less secure apps to access the Gmail account

### 4. Add environment variables
1. Create `.env` file in the root directory ./
2. Fill in accordingly below

<pre>
JWT_SECRET={can be any random string}
JWT_KEY={can be any random string}
MYSQL_ROOT_PASSWORD={root password, can be any random string}
MYSQL_DATABASE={database name, can be any random string}
MYSQL_USER={database username, can be any random string}
MYSQL_PASSWORD={database user password, can be any random string}
LOGDNA_INGESTION={LogDNA ingestion key}
EMAIL_USERNAME={gmail account ending with @gmail.com}
EMAIL_PASSWORD={gmail account password}
GOOGLE_BUCKET_NAME={GCP bucket name}
</pre>

### 5. Ensure you have Docker and NPM

### 6. Run locally
<pre>
#- backend -#
cd ./backend
docker-compose up --build

#- Frontend -#
cd ./frontend
npm i
npm run serve
</pre>

Following the steps above will run the backend microservices on port 8000 and frontend application on port 8080. Access `http://localhost:8080` for the application.