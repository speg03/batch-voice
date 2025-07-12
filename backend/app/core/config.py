import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_region: str = "us-east-1"
    aws_endpoint_url: str = "http://localhost:4566"
    
    s3_bucket_name: str = "batch-voice-files"
    dynamodb_users_table: str = "batch-voice-users"
    dynamodb_jobs_table: str = "batch-voice-jobs"
    dynamodb_results_table: str = "batch-voice-results"
    sqs_jobs_queue: str = "batch-voice-jobs"
    
    openai_api_key: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()