import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from app.models.schemas import JobResponse, JobStatus
from app.models.dynamodb import DynamoDBClient, JobModel, UserModel
from app.services import S3Service, SQSService

router = APIRouter()

async def get_db_client():
    return DynamoDBClient()

async def get_s3_service():
    return S3Service()

async def get_sqs_service():
    return SQSService()

@router.post("/jobs", response_model=JobResponse)
async def create_job(
    file: UploadFile = File(...),
    user_id: str = "default_user",
    db_client: DynamoDBClient = Depends(get_db_client),
    s3_service: S3Service = Depends(get_s3_service),
    sqs_service: SQSService = Depends(get_sqs_service)
):
    if not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Audio files only.")
    
    job_id = str(uuid.uuid4())
    
    try:
        file_path = await s3_service.upload_file(file, user_id)
        
        job_model = JobModel(db_client)
        job = await job_model.create_job(job_id, user_id, file.filename, file_path)
        
        await sqs_service.send_job_message(job_id, file_path)
        
        return JobResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            created_at=job['created_at']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")

@router.get("/jobs/{job_id}", response_model=dict)
async def get_job(
    job_id: str,
    db_client: DynamoDBClient = Depends(get_db_client)
):
    job_model = JobModel(db_client)
    job = await job_model.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job