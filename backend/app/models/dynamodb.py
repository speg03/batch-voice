import boto3
from datetime import datetime
from typing import Dict, List, Optional
from app.core.config import settings

class DynamoDBClient:
    def __init__(self):
        self.client = boto3.client(
            'dynamodb',
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.resource = boto3.resource(
            'dynamodb',
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )

class UserModel:
    def __init__(self, db_client: DynamoDBClient):
        self.db = db_client
        self.table = self.db.resource.Table(settings.dynamodb_users_table)
    
    async def create_user(self, user_id: str, email: str) -> Dict:
        now = datetime.utcnow().isoformat()
        item = {
            'user_id': user_id,
            'email': email,
            'created_at': now,
            'updated_at': now
        }
        self.table.put_item(Item=item)
        return item
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        response = self.table.get_item(Key={'user_id': user_id})
        return response.get('Item')

class JobModel:
    def __init__(self, db_client: DynamoDBClient):
        self.db = db_client
        self.table = self.db.resource.Table(settings.dynamodb_jobs_table)
    
    async def create_job(self, job_id: str, user_id: str, file_name: str, file_path: str) -> Dict:
        now = datetime.utcnow().isoformat()
        item = {
            'job_id': job_id,
            'user_id': user_id,
            'file_name': file_name,
            'file_path': file_path,
            'status': 'pending',
            'created_at': now,
            'updated_at': now
        }
        self.table.put_item(Item=item)
        return item
    
    async def get_job(self, job_id: str) -> Optional[Dict]:
        response = self.table.get_item(Key={'job_id': job_id})
        return response.get('Item')
    
    async def update_job_status(self, job_id: str, status: str, error_message: Optional[str] = None) -> Dict:
        now = datetime.utcnow().isoformat()
        update_expression = "SET #status = :status, updated_at = :updated_at"
        expression_values = {':status': status, ':updated_at': now}
        expression_names = {'#status': 'status'}
        
        if status == 'completed':
            update_expression += ", completed_at = :completed_at"
            expression_values[':completed_at'] = now
        
        if error_message:
            update_expression += ", error_message = :error_message"
            expression_values[':error_message'] = error_message
        
        response = self.table.update_item(
            Key={'job_id': job_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')

class ResultModel:
    def __init__(self, db_client: DynamoDBClient):
        self.db = db_client
        self.table = self.db.resource.Table(settings.dynamodb_results_table)
    
    async def create_result(self, result_id: str, job_id: str, transcription: str, confidence_score: Optional[float] = None) -> Dict:
        now = datetime.utcnow().isoformat()
        item = {
            'result_id': result_id,
            'job_id': job_id,
            'transcription': transcription,
            'created_at': now
        }
        if confidence_score:
            item['confidence_score'] = confidence_score
        
        self.table.put_item(Item=item)
        return item
    
    async def get_result_by_job(self, job_id: str) -> Optional[Dict]:
        response = self.table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('job_id').eq(job_id)
        )
        items = response.get('Items', [])
        return items[0] if items else None