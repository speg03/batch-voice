from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing" 
    COMPLETED = "completed"
    FAILED = "failed"

class User(BaseModel):
    user_id: str
    email: str
    created_at: datetime
    updated_at: datetime

class Job(BaseModel):
    job_id: str
    user_id: str
    file_name: str
    file_path: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class Result(BaseModel):
    result_id: str
    job_id: str
    transcription: str
    confidence_score: Optional[float] = None
    created_at: datetime

class JobCreate(BaseModel):
    file_name: str

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime