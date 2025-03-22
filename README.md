# Smart Warehouse Management System (AWS Free Tier)

## Project Description
This project is an **IoT-enabled Smart Warehouse Management System** built on AWS Free Tier. It simulates real-time inventory tracking using simulated IoT devices, AWS IoT Core, AWS Lambda, PostgreSQL, and React (hosted on AWS Amplify). The system allows users to monitor stock levels, track item movement, and predict shortages using AI models.

## Architecture Overview
1. **IoT Data Simulation (Python)** - Generates and publishes stock data to AWS IoT Core.
2. **AWS IoT Core & Lambda** - Processes incoming data and updates PostgreSQL database.
3. **PostgreSQL (RDS)** - Stores inventory logs.
4. **React Frontend (AWS Amplify)** - Displays inventory data in real-time.
5. **AI Forecasting (AWS SageMaker)** (Future Scope) - Predicts stock needs.
6. **Authentication (AWS Cognito)** (Future Scope) - User roles & access control.

---

## Components Breakdown

### AWS IoT Core
- Configured to receive messages from Python-based simulator.
- Connected to Lambda function for processing data.

### AWS Lambda Function (Database Insertion)
- Handles incoming requests, parses data, and inserts logs into PostgreSQL.
- Uses `pg8000` for database interaction.

### PostgreSQL (AWS RDS)
- Stores data in PostgreSQL
- Automatically scales with AWS Free Tier resources.

### React Frontend (AWS Amplify)
- Deployed via AWS Amplify Console.
- Connects to backend APIs using Axios.

### Simulated IoT Data Generator (Python)
- Publishes simulated stock movements to AWS IoT Core every 30 seconds.
- The above is done through terminal activation but future interation will be auto through EC2

---

## Setup Guide

### 1. Setting Up AWS RDS (PostgreSQL)
- Create a PostgreSQL instance.
- Configure security groups to allow Lambda access.
- Store credentials in AWS Secrets Manager or environment variables.

### 2. Deploying Lambda Function (Python)
- Create a Lambda function.
- Upload a zip file of the lambda fucntion.
- Add environment variables (`DB_ENDPOINT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`).
- Add layer AWSSDKPandas-Python39 to lambda function.

### 3. Setting Up AWS IoT Core
- Create a new IoT Thing.
- Generate certificates and policy.
- Attach policy to certificates and download them for local use.

### 4. Deploy React Frontend (AWS Amplify)
- Push your React project to a GitHub repository.
- Connect the repo to AWS Amplify.
- Deploy using Amplify Console (automatically rebuilds on pushes).

---

## 📌 How to Test
1. For IoT simulation, in AWS IoT, MQTT test client subscribe to topic warehouse/inventory
2. For Lambda, click the relevant function, then Test event
```sh
{
  "body": "{
    \"item_id\": 1,
    \"movement\": \"TEST\",
    \"quantity\": 10,
    \"timestamp\": \"2025-03-10T12:00:00Z\"
  }"
}
```