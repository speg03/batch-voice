import boto3
import uuid
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings

class S3Service:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.s3_bucket_name
    
    async def upload_file(self, file: UploadFile, user_id: str) -> str:
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        file_key = f"{user_id}/{uuid.uuid4()}.{file_extension}"
        
        self.client.upload_fileobj(
            file.file,
            self.bucket_name,
            file_key,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        return file_key
    
    async def get_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': file_key},
            ExpiresIn=expiration
        )

class SQSService:
    def __init__(self):
        self.client = boto3.client(
            'sqs',
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.queue_name = settings.sqs_jobs_queue
        self.queue_url = None
    
    async def get_queue_url(self) -> str:
        if not self.queue_url:
            response = self.client.get_queue_url(QueueName=self.queue_name)
            self.queue_url = response['QueueUrl']
        return self.queue_url
    
    async def send_job_message(self, job_id: str, file_path: str) -> dict:
        queue_url = await self.get_queue_url()
        message_body = {
            'job_id': job_id,
            'file_path': file_path,
            'action': 'transcribe'
        }
        
        response = self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=str(message_body)
        )
        
        return response