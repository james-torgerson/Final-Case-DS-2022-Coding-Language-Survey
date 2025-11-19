from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    role: str = Field(..., min_length=1, max_length=100)
    languages: list[str] = Field(..., min_items=1)
    proficiencies: Optional[dict[str, str]] = None
    submission_id: Optional[str] = None

    @validator('proficiencies', pre=True, always=True)
    def validate_proficiencies(cls, v, values): 
        if 'languages' in values and v is not None:
            for lang in values['languages']:
                if lang not in v:
                    raise ValueError(f'Proficiency for language {lang} is missing')
        return v
    
#Good example of inheritance
class StoredSurveyRecord(SurveySubmission):
    name: str 
    email: Optional[str]
    email_hash: str
    role: str
    languages: list[str]
    submission_id: Optional[str]
    received_at: datetime
    ip: str

    class Config:
            fields = {
                'email': {'exclude': True},
            }