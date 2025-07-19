#!/usr/bin/env bash

# Set AWS CLI to use LocalStack
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_PAGER=""

# Scan DynamoDB jobs table
echo "Scanning batch-voice-jobs table..."
aws --endpoint-url=$AWS_ENDPOINT_URL dynamodb scan --table-name batch-voice-jobs
if [ $? -ne 0 ]; then
    echo "Failed to scan batch-voice-jobs table. Please ensure the table exists and LocalStack is running."
    exit 1
fi
