#!/bin/bash

# Setup LocalStack resources for batch-voice project

set -e

echo "Setting up LocalStack resources..."

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
sleep 5

# Set AWS CLI to use LocalStack
export AWS_ENDPOINT_URL=http://localhost:4566
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

# Create S3 bucket
echo "Creating S3 bucket..."
aws --endpoint-url=$AWS_ENDPOINT_URL s3 mb s3://batch-voice-files || echo "Bucket already exists"

# Create SQS queue
echo "Creating SQS queue..."
aws --endpoint-url=$AWS_ENDPOINT_URL sqs create-queue --queue-name batch-voice-jobs || echo "Queue already exists"

# Create DynamoDB tables
echo "Creating DynamoDB tables..."

# Users table
aws --endpoint-url=$AWS_ENDPOINT_URL dynamodb create-table \
    --table-name batch-voice-users \
    --attribute-definitions \
        AttributeName=user_id,AttributeType=S \
    --key-schema \
        AttributeName=user_id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region ap-northeast-1 || echo "Users table already exists"

# Jobs table
aws --endpoint-url=$AWS_ENDPOINT_URL dynamodb create-table \
    --table-name batch-voice-jobs \
    --attribute-definitions \
        AttributeName=job_id,AttributeType=S \
        AttributeName=user_id,AttributeType=S \
        AttributeName=created_at,AttributeType=S \
    --key-schema \
        AttributeName=job_id,KeyType=HASH \
        AttributeName=user_id,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --global-secondary-indexes \
        'IndexName=user_id-created_at-index,KeySchema=[{AttributeName=user_id,KeyType=HASH},{AttributeName=created_at,KeyType=RANGE}],Projection={ProjectionType=ALL},ProvisionedThroughput={ReadCapacityUnits=5,WriteCapacityUnits=5}' \
    --region ap-northeast-1 || echo "Jobs table already exists"

# Results table
aws --endpoint-url=$AWS_ENDPOINT_URL dynamodb create-table \
    --table-name batch-voice-results \
    --attribute-definitions \
        AttributeName=job_id,AttributeType=S \
    --key-schema \
        AttributeName=job_id,KeyType=HASH \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region ap-northeast-1 || echo "Results table already exists"

echo "LocalStack setup completed!"
echo ""
echo "Access LocalStack Web UI: http://localhost:4566"
echo "S3 Bucket: batch-voice-files"
echo "SQS Queue: batch-voice-jobs"
echo "DynamoDB Tables: batch-voice-users, batch-voice-jobs, batch-voice-results"